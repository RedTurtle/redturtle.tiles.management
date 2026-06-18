// src/patterns/tiles-management/tiles-management.js

import BasePattern from "@patternslib/patternslib/src/core/basepattern";
import Parser from "@patternslib/patternslib/src/core/parser";
import registry from "@patternslib/patternslib/src/core/registry";
import Sortable from "sortablejs";

export const parser = new Parser("tiles-management");
parser.addArgument("managerId", null);

class Pattern extends BasePattern {
    static name = "tiles-management";
    static trigger = ".pat-tiles-management";
    static parser = parser;

    async init() {
        import("./tiles-management.scss");
        // Patternslib converte 'manager-id' da HTML/parser in 'managerId' qui.
        this.managerId = this.options.managerId;

        if (!this.managerId) {
            this.el.innerHTML = `<p class="error">Errore: l'attributo 'data-pat-tiles-management' deve specificare un manager-id.</p>`;
            return;
        }

        this._observeModalForms();

        await this._loadManager();
    }

    _observeModalForms() {
        if (this._modalFormsObserver) {
            return;
        }

        // Track the last tile-management link clicked within THIS instance's element.
        // This lets us know which managerId owns the modal that is about to open.
        this._lastClickedTileLink = null;
        this._tileLinksClickHandler = (event) => {
            const link = event.target.closest(
                'a[href*="/@@add-tile/"], a[href*="@@delete-tile"], a.tileDeleteLink',
            );
            if (link && this.el.contains(link)) {
                this._lastClickedTileLink = link;
            }
        };
        document.addEventListener("click", this._tileLinksClickHandler, true);

        this._modalFormsObserver = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                mutation.addedNodes.forEach((node) => {
                    if (!(node instanceof Element)) {
                        return;
                    }

                    const forms = [];
                    if (node.matches("form") && this._isTilesManagementForm(node)) {
                        forms.push(node);
                    }
                    node.querySelectorAll("form").forEach((f) => {
                        if (this._isTilesManagementForm(f)) {
                            forms.push(f);
                        }
                    });

                    forms.forEach((form) => {
                        if (form instanceof HTMLFormElement) {
                            this._normalizeTilesManagementForm(form);
                        }
                    });
                });
            });
        });

        this._modalFormsObserver.observe(document.body, {
            childList: true,
            subtree: true,
        });
    }

    _normalizeTilesManagementForm(form) {
        this._ensureManagerIdInput(form);
        this._removeManagerIdFromFormAction(form);
        // Reset after normalization so the next modal open is evaluated fresh.
        this._lastClickedTileLink = null;
    }

    _ensureManagerIdInput(form) {
        if (!this.managerId) {
            return;
        }

        let managerField = form.querySelector('input[name="managerId"]');
        if (!managerField) {
            managerField = document.createElement("input");
            managerField.type = "hidden";
            managerField.name = "managerId";
            form.appendChild(managerField);
        }

        managerField.value = this.managerId;
    }

    _removeManagerIdFromFormAction(form) {
        if (!form?.action) {
            return;
        }

        try {
            const actionUrl = new URL(form.action, window.location.href);
            if (!actionUrl.searchParams.has("managerId")) {
                return;
            }

            actionUrl.searchParams.delete("managerId");
            form.action = actionUrl.toString();
        } catch (err) {
            // Ignore malformed URLs and keep current form action.
        }
    }

    _isTilesManagementForm(form) {
        if (!(form instanceof HTMLFormElement)) {
            return false;
        }

        const matchesById = form.id === "add_tile" || form.id === "delete_tile";
        const action = form.getAttribute("action") || "";
        const matchesByAction =
            action.includes("/@@add-tile/") || action.includes("@@delete-tile");

        if (!matchesById && !matchesByAction) {
            return false;
        }

        // Primary check: the last tile link clicked was inside this instance's element.
        // This is the most reliable way to know which managerId owns this modal,
        // and avoids conflicts when multiple pat-tiles-management instances are on the page.
        if (this._lastClickedTileLink !== null) {
            return this.el.contains(this._lastClickedTileLink);
        }

        // Fallback: check managerId in form action URL.
        try {
            const actionUrl = new URL(form.action, window.location.href);
            const formManagerId = actionUrl.searchParams.get("managerId");
            if (formManagerId) {
                return formManagerId === this.managerId;
            }
        } catch (e) {
            // ignore malformed URLs
        }

        // Fallback: check hidden input already injected.
        const managerInput = form.querySelector('input[name="managerId"]');
        if (managerInput?.value) {
            return managerInput.value === this.managerId;
        }

        return true;
    }

    _decorateTileModalLinksWithManagerId() {
        const selectors = [
            'a[href*="/@@add-tile/"]',
            'a[href*="@@delete-tile"]',
            "a.tileDeleteLink",
        ];
        this.el.querySelectorAll(selectors.join(", ")).forEach((link) => {
            this._ensureManagerIdInLinkHref(link);
        });
    }

    _ensureManagerIdInLinkHref(link) {
        if (!this.managerId || !(link instanceof HTMLAnchorElement) || !link.href) {
            return;
        }

        try {
            const hrefUrl = new URL(link.href, window.location.href);
            if (hrefUrl.searchParams.get("managerId") === this.managerId) {
                return;
            }
            hrefUrl.searchParams.set("managerId", this.managerId);
            link.href = hrefUrl.toString();
        } catch (err) {
            // Ignore malformed link href.
        }
    }

    async _loadManager() {
        this.el.innerHTML =
            '<div class="spinner-border" role="status"><span class="visually-hidden">Loading...</span></div>';

        const baseUrl = document.body.dataset.baseUrl || "";
        const url = new URL(`${baseUrl}/tiles_management`);
        url.searchParams.append("managerId", this.managerId);
        url.searchParams.append("ajax_load", "1");

        try {
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error(`Errore di rete: ${response.statusText}`);
            }
            const html = await response.text();

            if (!html.trim()) {
                this.el.remove();
                return;
            }
            // Creiamo un contenitore temporaneo per manipolare l'HTML
            const tempDiv = document.createElement("div");
            tempDiv.innerHTML = html;

            // Troviamo e rimuoviamo tutti i trigger .pat-tiles-management ANNIDATI
            // per evitare il loop ricorsivo.
            const nestedTriggers = tempDiv.querySelectorAll(".pat-tiles-management");
            nestedTriggers.forEach((trigger) => trigger.remove());

            // Ora svuotiamo this.el e aggiungiamo il contenuto "pulito"
            this.el.innerHTML = "";
            while (tempDiv.firstChild) {
                this.el.appendChild(tempDiv.firstChild);
            }

            this.el.dispatchEvent(new CustomEvent("rtTilesLoaded", { bubbles: true }));
            this._enableInteractions();
            registry.scan(this.el);
        } catch (err) {
            console.error("Impossibile caricare il gestore dei tile:", err);
            this.el.innerHTML = `<p class="error-manager">Si è verificato un errore durante il caricamento.</p>`;
        }
    }

    _enableInteractions() {
        this._decorateTileModalLinksWithManagerId();

        const addTileButton = this.el.querySelector(".add-tile-btn");
        if (addTileButton) {
            addTileButton.addEventListener("click", (e) => {
                e.preventDefault();
                this._initializeAddButton(addTileButton, e.currentTarget.href);
            });
        }

        this.el.querySelectorAll(".tilesList .tileWrapper").forEach((tile) => {
            this._enableTileHover(tile);
            this._enableAjaxLinks(tile);
        });

        if (window.innerWidth > 991) {
            this._enableSorting();
        }
    }

    async _initializeAddButton(button, url) {
        let container = button.nextElementSibling;
        if (!container || !container.classList.contains("available-tiles")) {
            button.parentElement.insertAdjacentHTML(
                "beforeend",
                '<div class="available-tiles" style="display: none;"></div>',
            );
            container = button.nextElementSibling;

            try {
                const response = await fetch(url);
                const text = await response.text();
                const tempDiv = document.createElement("div");
                tempDiv.innerHTML = text;
                const tilesList = tempDiv.querySelector("#content .list-group");

                if (tilesList) {
                    // FIX 2: Usa appendChild per includere il div.list-group wrapper.
                    container.innerHTML = ""; // Pulisci prima il contenitore
                    container.appendChild(tilesList);
                    container.querySelectorAll("a.list-group-item").forEach((link) => {
                        this._ensureManagerIdInLinkHref(link);
                        const modalOptions = {
                            actionOptions: {
                                redirectOnResponse: true,
                                redirectToUrl: window.location.href,
                                data: { managerId: this.managerId },
                            },
                            templateOptions: {
                                className: "modal fade tiles-management-modal",
                            },
                        };
                        link.dataset.patModal = JSON.stringify(modalOptions);
                    });

                    registry.scan(container);
                }
                container.style.display = "block";
            } catch (err) {
                console.error("Errore nel caricamento dei tile disponibili:", err);
            }
        } else {
            container.style.display =
                container.style.display === "none" ? "block" : "none";
        }
    }

    _enableAjaxLinks(tile) {
        const links = tile.querySelectorAll(
            "div.tileEditButtons a.tileVisibilityLink, div.tileEditButtons .tileSizeLink a.dropdown-item",
        );
        links.forEach((link) => {
            link.addEventListener("click", async (e) => {
                e.preventDefault();
                const url = new URL(e.currentTarget.href);
                url.searchParams.append("managerId", this.managerId);
                url.searchParams.append("ajax_load", "1");

                try {
                    await fetch(url);
                    await this._loadManager();
                } catch (err) {
                    console.error("Errore durante l'aggiornamento del tile:", err);
                }
            });
        });
    }

    _enableTileHover(tile) {
        const editButtons = tile.querySelector(".tileEditButtons");
        if (editButtons) {
            editButtons.style.display = "none";
            tile.addEventListener("mouseenter", () => {
                tile.classList.add("editableTile");
                editButtons.style.display = "block";
            });
            tile.addEventListener("mouseleave", () => {
                tile.classList.remove("editableTile");
                editButtons.style.display = "none";
            });
        }
    }

    _enableSorting() {
        const tilesList = this.el.querySelector(".tilesList");
        if (tilesList) {
            Sortable.create(tilesList, {
                draggable: "div.tileWrapper",
                animation: 200,
                onUpdate: async (data) => {
                    const tileIds = Array.from(data.to.children).map(
                        (el) => el.dataset.tileid,
                    );
                    const absoluteUrl = document.body.dataset.baseUrl || "";
                    const url = new URL(`${absoluteUrl}/reorder_tiles`);
                    url.searchParams.append("managerId", this.managerId);
                    url.searchParams.append("ajax_load", "1");
                    url.searchParams.append("tileIds", JSON.stringify(tileIds));
                    try {
                        const response = await fetch(url);
                        if (response.status === 204) {
                            return;
                        }
                        if (!response.ok) {
                            const errorData = await response.json().catch(() => null);
                            const errorMessage =
                                errorData?.message || `Errore HTTP: ${response.status}`;
                            throw new Error(errorMessage);
                        }
                        const data = await response.json();
                        if (data && data.message) {
                            console.error(data.message);
                        }
                    } catch (err) {
                        console.error("Errore durante il riordino dei tile:", err);
                    }
                },
            });
        }
    }
}

registry.register(Pattern);

export default Pattern;
export { Pattern };

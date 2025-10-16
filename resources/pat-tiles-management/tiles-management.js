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
            console.error("manager-id non fornito per pat-tiles-management", this.el);
            return;
        }

        await this._loadManager();
    }

    async _loadManager() {
        const portalUrl = document.body.dataset.portalUrl || "";
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

            this.el.innerHTML = html;
            this.el.dispatchEvent(new CustomEvent("rtTilesLoaded", { bubbles: true }));
            this._enableInteractions();
            registry.scan(this.el);
        } catch (err) {
            console.error("Impossibile caricare il gestore dei tile:", err);
            this.el.innerHTML = `<p class="error-manager">Si è verificato un errore durante il caricamento.</p>`;
        }
    }

    _enableInteractions() {
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
                '<div class="available-tiles" style="display: none;"></div>'
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
            "div.tileEditButtons a.tileVisibilityLink, div.tileEditButtons .tileSizeLink a.dropdown-item"
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
        Sortable.create(this.el.querySelector(".tilesList"), {
            draggable: "div.tileWrapper",
            animation: 200,
            onUpdate: async (data) => {
                const tileIds = Array.from(data.to.children).map(
                    (el) => el.dataset.tileid
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

registry.register(Pattern);

export default Pattern;
export { Pattern };

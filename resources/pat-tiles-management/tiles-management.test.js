import Pattern from "./tiles-management";
import utils from "@patternslib/patternslib/src/core/utils";

describe("pat-tiles-management", () => {
    beforeEach(() => {
        document.body.innerHTML = "";
    });

    it("is initialized correctly", async () => {
        document.body.innerHTML = `<div class="pat-tiles-management" />`;
        const el = document.querySelector(".pat-tiles-management");

        const instance = new Pattern(el);
        await utils.timeout(1); // wait a tick for async to settle.

        expect(el.innerHTML.trim()).toBe(
            `<p>hello ${instance.options.exampleOption}, this is pattern ${instance.name} speaking.</p>`
        );
    });
    it("is initialized correctly with options from attribute", async () => {
        document.body.innerHTML = `<div
            class="pat-tiles-management"
            data-pat-tiles-management='{"example-option": "World"}'
            />`;
        const el = document.querySelector(".pat-tiles-management");

        const instance = new Pattern(el);
        await utils.timeout(1); // wait a tick for async to settle.

        expect(el.innerHTML.trim()).toBe(
            `<p>hello World, this is pattern ${instance.name} speaking.</p>`
        );
    });
});

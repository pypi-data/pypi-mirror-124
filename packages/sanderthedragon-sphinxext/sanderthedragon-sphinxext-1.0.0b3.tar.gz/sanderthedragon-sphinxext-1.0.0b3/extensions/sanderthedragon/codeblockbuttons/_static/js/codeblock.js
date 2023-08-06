/*
 * SPDX-FileCopyrightText: 2021 SanderTheDragon <sanderthedragon@zoho.com>
 *
 * SPDX-License-Identifier: MIT
 */

let ids = [];

// Generate an unique ID
function generateID() {
    const id = Math.random().toString(36).substr(2);
    if (ids.includes(id)) {
        return generateID();
    }

    ids.push(id);

    return id;
}

// From "https://tablericons.com", licensed under MIT
let icons = {
    "code": "PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIGNsYXNzPSJpY29uLXRhYmxlciBpY29uLXRhYmxlci1jb2RlIiB2aWV3Qm94PSIwIDAgMjQgMjQiIHN0cm9rZS13aWR0aD0iMS41IiBzdHJva2U9IiMwMDAwMDAiIGZpbGw9Im5vbmUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCI+CiAgPHBhdGggc3Ryb2tlPSJub25lIiBkPSJNMCAwaDI0djI0SDB6IiBmaWxsPSJub25lIi8+CiAgPHBvbHlsaW5lIHBvaW50cz0iNyA4IDMgMTIgNyAxNiIgLz4KICA8cG9seWxpbmUgcG9pbnRzPSIxNyA4IDIxIDEyIDE3IDE2IiAvPgogIDxsaW5lIHgxPSIxNCIgeTE9IjQiIHgyPSIxMCIgeTI9IjIwIiAvPgo8L3N2Zz4=",
    "copy": "PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIGNsYXNzPSJpY29uLXRhYmxlciBpY29uLXRhYmxlci1jb3B5IiB2aWV3Qm94PSIwIDAgMjQgMjQiIHN0cm9rZS13aWR0aD0iMS41IiBzdHJva2U9IiMwMDAwMDAiIGZpbGw9Im5vbmUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCI+CiAgPHBhdGggc3Ryb2tlPSJub25lIiBkPSJNMCAwaDI0djI0SDB6IiBmaWxsPSJub25lIi8+CiAgPHJlY3QgeD0iOCIgeT0iOCIgd2lkdGg9IjEyIiBoZWlnaHQ9IjEyIiByeD0iMiIgLz4KICA8cGF0aCBkPSJNMTYgOHYtMmEyIDIgMCAwIDAgLTIgLTJoLThhMiAyIDAgMCAwIC0yIDJ2OGEyIDIgMCAwIDAgMiAyaDIiIC8+Cjwvc3ZnPg==",
    "copy-error": "PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIGNsYXNzPSJpY29uLXRhYmxlciBpY29uLXRhYmxlci1jbGlwYm9hcmQteCIgdmlld0JveD0iMCAwIDI0IDI0IiBzdHJva2Utd2lkdGg9IjEuNSIgc3Ryb2tlPSIjMDAwMDAwIiBmaWxsPSJub25lIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiPgogIDxwYXRoIHN0cm9rZT0ibm9uZSIgZD0iTTAgMGgyNHYyNEgweiIgZmlsbD0ibm9uZSIvPgogIDxwYXRoIGQ9Ik05IDVoLTJhMiAyIDAgMCAwIC0yIDJ2MTJhMiAyIDAgMCAwIDIgMmgxMGEyIDIgMCAwIDAgMiAtMnYtMTJhMiAyIDAgMCAwIC0yIC0yaC0yIiAvPgogIDxyZWN0IHg9IjkiIHk9IjMiIHdpZHRoPSI2IiBoZWlnaHQ9IjQiIHJ4PSIyIiAvPgogIDxwYXRoIGQ9Ik0xMCAxMmw0IDRtMCAtNGwtNCA0IiAvPgo8L3N2Zz4=",
    "copy-success": "PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIGNsYXNzPSJpY29uLXRhYmxlciBpY29uLXRhYmxlci1jbGlwYm9hcmQtY2hlY2siIHZpZXdCb3g9IjAgMCAyNCAyNCIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZT0iIzAwMDAwMCIgZmlsbD0ibm9uZSIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIj4KICA8cGF0aCBzdHJva2U9Im5vbmUiIGQ9Ik0wIDBoMjR2MjRIMHoiIGZpbGw9Im5vbmUiLz4KICA8cGF0aCBkPSJNOSA1aC0yYTIgMiAwIDAgMCAtMiAydjEyYTIgMiAwIDAgMCAyIDJoMTBhMiAyIDAgMCAwIDIgLTJ2LTEyYTIgMiAwIDAgMCAtMiAtMmgtMiIgLz4KICA8cmVjdCB4PSI5IiB5PSIzIiB3aWR0aD0iNiIgaGVpZ2h0PSI0IiByeD0iMiIgLz4KICA8cGF0aCBkPSJNOSAxNGwyIDJsNCAtNCIgLz4KPC9zdmc+"
};

// Set an SVG icon from base64
function setSVG(element, ico) {
    let icon = element.querySelector(":scope > div.cb-icon");
    if (icon == null) {
        icon = document.createElement("div");
        icon.classList.add("cb-icon");

        element.appendChild(icon);
    }

    icon.innerHTML = atob(icons[ico]);
}

// Set a tooltip
function setTooltip(element, text) {
    let tooltip = element.querySelector(":scope > span.cb-tooltip");
    if (tooltip == null) {
        tooltip = document.createElement("span");
        tooltip.classList.add("cb-tooltip");

        element.appendChild(tooltip);
    }

    tooltip.innerHTML = text;
}

// Add controls to a code block
function addControls(element) {
    element.id = `_${generateID()}`;

    // Add nothing to code blocks with the `cb-none` class
    if (element.parentElement.classList.contains("cb-none")) {
        return;
    }

    // Add the copy button, if `cb-nocopy` is not defined
    if (!element.parentElement.classList.contains("cb-nocopy")) {
        let copyButton = document.createElement("div");
        copyButton.classList.add("cb-button");
        copyButton.id = "cb-copy";
        copyButton.setAttribute("data-clipboard-target",
                                `#${element.id} > pre`);
        setSVG(copyButton, "copy");
        setTooltip(copyButton, "Copy");
        element.appendChild(copyButton);
    }

    // Add the view button, if `cb-noview` is not defined
    if (!element.parentElement.classList.contains("cb-noview")) {
        let viewButton = document.createElement("div");
        viewButton.classList.add("cb-button");
        viewButton.id = "cb-view";
        setSVG(viewButton, "code");
        setTooltip(viewButton, "View");
        element.appendChild(viewButton);

        // Create a blob from the content of the code block, and then open it
        viewButton.addEventListener("click", function() {
            const data = element.querySelector("pre").innerText;
            const file = new Blob([ data ], { type: "text/plain" });
            const url = URL.createObjectURL(file);
            window.open(url);
        });
    }

    // Make the scroll area large enough for the buttons to not overlay the code
    const buttonCount = element.getElementsByClassName("cb-button").length;
    if (buttonCount > 0) {
        const position = element.innerHTML.indexOf('\n');
        element.innerHTML = element.innerHTML.slice(0, position)
                          + `<span class="cb-pad cb-pad-${buttonCount}"></span>`
                          + element.innerHTML.slice(position);
    }
}

// Reset the copy button from success (or error) to normal
function resetCopyOnLeave(event) {
    const element = event.trigger;
    element.addEventListener("mouseleave", function _rc() {
        setSVG(element, "copy");
        setTooltip(element, "Copy");
        element.removeEventListener("mouseleave", _rc);
    });
}

document.addEventListener("DOMContentLoaded", function() {
    // Iterate over all code blocks
    const elements = document.querySelectorAll("div.highlight");
    elements.forEach(function(element) {
        addControls(element);
    });

    // Create an instance of `ClipboardJS` for `cb-button`s
    const clipboard = new ClipboardJS("div.cb-button");

    clipboard.on("success", function(event) {
        event.clearSelection();

        const element = event.trigger;
        setSVG(element, "copy-success");
        setTooltip(element, "Copied");
        resetCopyOnLeave(event);
    });

    clipboard.on("error", function(event) {
        const element = event.trigger;
        setSVG(element, "copy-error");
        setTooltip(element, "Failed");
        resetCopyOnLeave(event);
    });
});

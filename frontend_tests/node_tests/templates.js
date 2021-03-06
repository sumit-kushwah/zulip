"use strict";

const {strict: assert} = require("assert");

const {JSDOM} = require("jsdom");

const {set_global, zrequire} = require("../zjsunit/namespace");
const {run_test} = require("../zjsunit/test");

set_global("DOMParser", new JSDOM().window.DOMParser);
zrequire("templates");

run_test("and", () => {
    const args = {
        last: true,
    };

    const html = require("./templates/and.hbs")(args);
    assert.equal(html, "<p>empty and</p>\n<p>last and</p>\n\n");
});

run_test("or", () => {
    const args = {
        last: true,
    };

    const html = require("./templates/or.hbs")(args);
    assert.equal(html, "\n<p>last or</p>\n<p>true or</p>\n");
});

run_test("let", () => {
    const html = require("./templates/let.hbs")({
        outer_var: "hello",
    });
    assert.equal(
        html,
        `\
    outer_var = hello
    keyword_var = &lt;b&gt;escaped&lt;/b&gt;
    block_var =     <b>unescaped</b> with hello

`,
    );
});

run_test("rendered_markdown", () => {
    const html = require("./templates/rendered_markdown.hbs")();
    const expected_html =
        '<a href="http://example.com" target="_blank" rel="noopener noreferrer" title="http://example.com/">good</a>\n';
    assert.equal(html, expected_html);
});

run_test("numberFormat", () => {
    const args = {
        number: 1000000,
    };

    const html = require("./templates/numberFormat.hbs")(args);
    assert.equal(html, "1,000,000\n");
});

# Markdown

## Background

!!! info  "Disclaimer"
    This styleguide is heavily inspired of [Google Markdown Style
    Guide][google_markdown_styleguide] , most part come directly from it.

    **Nevertheless, it  differs in some ways, mainly adding more requirements.
    Please read carefully.**

[google_markdown_styleguide]: https://google.github.io/styleguide/docguide/style.html

## Introduction

Much of what makes Markdown great is the ability to write plain text, and get
great formatted output as a result. To keep the slate clean for the next
author, your Markdown should be simple and consistent with the whole corpus
wherever possible.

We seek to balance three goals:

- Source text is readable and portable.
- Markdown files are maintainable over time and across teams.
- The syntax is simple and easy to remember.


## Document layout

In general, most documents benefit from some variation of the following layout:

```markdown
# Document Title

Short introduction.

[TOC]

## Topic

Content.

## See also

* https://link-to-more-info

```

1. `# Document Title`: The first heading should be a level one heading, and
   should ideally be the same or nearly the same as the filename. The first
   level one heading is used as the page `<title>`,
2. `Short introduction.`: 1-3 sentences providing a high-level overview of
   the topic. Imagine yourself as a complete newbie, who landed on your
   “Extending Foo” doc and needs to know the most basic assumptions you take for
   granted. “What is Foo? Why would I extend it?”,
3. `[TOC]`: if you use hosting that supports table of contents, put the
   supported `[TOC]` tag after the short introduction. You can also "manually"
   add a table of content from your favorite text editor if you have plugins
   allowing to do so (like [vim-markdown-toc][vim_markdown_toc]). Note that in
   case of markdown files used with [mkdocs][mkdocs], there is no nedd to add
   any `[TOC]` tag as table of content is autmatically handled with
   [mkdocs][mkdocs],
4. `## Topic`: The rest of your headings should start from level 2.
5. `## See also`: Put miscellaneous links at the bottom for the user who
   wants to know more or didn’t find what she needed.

[vim_markdown_toc]: https://github.com/mzlogin/vim-markdown-toc

## Character line limit

Obey projects’ character line limit wherever possible. Long URLs and tables are
the usual suspects when breaking the rule. (Headings also can’t be wrapped, but
we encourage keeping them short). Otherwise, wrap your text:

```markdown
Lorem ipsum dolor sit amet, nec eius volumus patrioque cu, nec et commodo
hendrerit, id nobis saperet fuisset ius.

*   Malorum moderatius vim eu. In vix dico persecuti. Te nam saperet percipitur
    interesset. See the [foo docs](https://domain.tld/very/long/link/which-are-greater-that-line-limit)
```

Often, inserting a newline before a long link preserves readability while
minimizing the overflow:

```markdown
Lorem ipsum dolor sit amet. See the
[foo docs](https://domain.tld/very/long/link/which-are-greater-that-line-limit)
for details.
```

## Trailing whitespace

Don’t use trailing whitespace, use a trailing backslash.

The [CommonMark spec][commonmark_spec] decrees that two spaces at the end of a
line should insert a `<br/>` tag. However, many directories have a trailing
whitespace presubmit check in place, and many IDEs will clean it up anyway.

Best practice is to avoid the need for a `<br/>` altogether. Markdown creates
paragraph tags for you simply with newlines: get used to that.

[commonmark_spec]: https://spec.commonmark.org/0.20/#hard-line-breaks

## Headings

### ATX-style headings

```markdown
## Heading 2
```

Headings with `=` or `-` underlines can be annoying to maintain and don’t fit
with the rest of the heading syntax. The user has to ask: Does `---` mean H1 or
H2?

```markdown
Heading - do you remember what level? DO NOT DO THIS.
---------
```

### Add spacing to headings

Prefer spacing after # and newlines before and after:

```markdown
...text before.

# Heading 1

Text after...
```

Lack of spacing makes it a little harder to read in source:

```markdown
...text before.

#Heading 1
Text after... DO NOT DO THIS.
```

## Lists

### Use lazy numbering for long lists

Markdown is smart enough to let the resulting HTML render your numbered lists
correctly. For longer lists that may change, especially long nested lists, use
“lazy” numbering:

```markdown
1.  Foo.
1.  Bar.
    1.  Foofoo.
    1.  Barbar.
1.  Baz.
```

However, if the list is small and you don’t anticipate changing it, prefer fully numbered lists, because it’s nicer to read in source:

```markdown
1.  Foo.
2.  Bar.
3.  Baz.
```

### Nested list spacing

When nesting lists, use a 4 space indent for both numbered and bulleted lists:

```markdown
1.  2 spaces after a numbered list.
    4 space indent for wrapped text.
2.  2 spaces again.

*   3 spaces after a bullet.
    4 space indent for wrapped text.
    1.  2 spaces after a numbered list.
        8 space indent for the wrapped text of a nested list.
    2.  Looks nice, don't it?
*   3 spaces after a bullet.
```

The following works, but it’s very messy:

```markdown
* One space,
with no indent for wrapped text.
     1. Irregular nesting... DO NOT DO THIS.
```

Even when there’s no nesting, using the 4 space indent makes layout consistent
for wrapped text:

```markdown
*   Foo,
    wrapped.

1.  2 spaces
    and 4 space indenting.
2.  2 spaces again.
```

However, when lists are small, not nested, and a single line, one space can
suffice for both kinds of lists:

```markdown
* Foo
* Bar
* Baz.

1. Foo.
2. Bar.
```

## Code

### Inline

\`Backticks\` designate `inline code`, and will render all wrapped content
literally. Use them for short code quotations and field names:

```markdown
You'll want to run `really_cool_script.sh arg`.

Pay attention to the `foo_bar_whammy` field in that table.
```

Use inline code when referring to file types in an abstract sense, rather than a
specific file:

```markdown
Be sure to update your `README.md`!
```

Backticks are the most common approach for “escaping” Markdown metacharacters;
in most situations where escaping would be needed, code font just makes sense
anyway.

### Codeblocks

For code quotations longer than a single line, use a codeblock:

```markdown
 ```python
 def Foo(self, bar):
   self.bar = bar
 ```
```

#### Declare the language

It is best practice to explicitly declare the language, so that neither the
syntax highlighter nor the next editor must guess.

#### Indented codeblocks are sometimes cleaner

Four-space indenting is also interpreted as a codeblock. These can look cleaner
and be easier to read in source, but there is no way to specify the language. We
encourage their use when writing many short snippets:

```markdown
You'll need to run:

    bazel run :thing -- --foo

And then:

    bazel run :another_thing -- --bar

And again:

    bazel run :yet_again -- --baz
```

#### Escape newlines

Because most commandline snippets are intended to be copied and pasted directly into a terminal, it’s best practice to escape any newlines. Use a single backslash at the end of the line:

```markdown
 ```shell
 bazel run :target -- --flag --foo=longlonglonglonglongvalue \
 --bar=anotherlonglonglonglonglonglonglonglonglonglongvalue
 ```
```

### Nest codeblocks within lists

If you need a codeblock within a list, make sure to indent it so as to not break the list:

```markdown
*   Bullet.

    ```c++
    int foo;
    ```

*   Next bullet.
```

You can also create a nested code block with 4 spaces. Simply indent 4 additional spaces from the list indentation:

```markdown
*   Bullet.

        int foo;

*   Next bullet.
```

### Links

Long links make source Markdown difficult to read and break the 80 character
wrapping. **Wherever possible, shorten your links.**

### Use informative Markdown link titles

Markdown link syntax allows you to set a link title, just as HTML does. Use it
wisely.

Titling your links as “link” or “here” tells the reader precisely nothing when
quickly scanning your doc and is a waste of space:

```markdown
See the syntax guide for more info: [link](syntax_guide.md).
Or, check out the style guide [here](style_guide.md).
DO NOT DO THIS.
```

Instead, write the sentence naturally, then go back and wrap the most
appropriate phrase with the link:

```markdown
See the [syntax guide](syntax_guide.md) for more info.
Or, check out the [style guide](style_guide.md).
```

Or even better, use [link reference definitions][link_ref_def] and put the link
definition at the end of the current chapter unless link definition is used
elsewhere:

```markdown
# Chapter 1

See the [syntax guide][syntax_guide] for more info.
Or check out the [style guide][style_guide].

[syntax_guide]: syntax_guide.md

# Chapter 2

You will see in [style guide][style_guide] some tutorials to help you apply it.

[style_guide]: style_guide.md
```

This aim of this usage is to avoid needed to update same link multiple times as
only link definition will need to be updte. Moreover, if a link defintion is at
the end of the chapter means the link is only used within the chapter. While a
link definition at the end a of file means the link is used multiple times in
the file.

[link_ref_def]: https://spec.commonmark.org/0.29/#link-reference-definitions

## Images

Use images sparingly, and prefer simple screenshots. This guide is designed
around the idea that plain text gets users down to the business of communication
faster with less reader distraction and author procrastination. However, it’s
sometimes very helpful to show what you mean.

Use of image is similar to links but begin with `!` to denote an image
reference:

```markdown
Use image link directly :

![diffy the kung fu review cuckoo](http://absolute.link/to/image.png)

Use image link references (preferred method):
![diffy the kung fu review cuckoo][img_diffy]

[img_diff]: http://absolute.link/to/image.png
```

Image source can be either:

- Absolute URLs beginning with https:// and http://
- Relative URLs

Such value will be used as written for the `<img src="...">`

Malformed URLs will be replaced with a broken data: reference to prevent browsers from trying to load a bad destination.

## Prefer lists to tables

Any tables in your Markdown should be small. Complex, large tables are difficult
to read in source and most importantly, a pain to modify later.

```markdown
Fruit | Attribute | Notes
--- | --- | --- | ---
Apple | [Juicy](https://example.com/SomeReallyReallyReallyReallyReallyReallyReallyReallyLongQuery), Firm, Sweet | Apples keep doctors away.
Banana | [Convenient](https://example.com/SomeDifferentReallyReallyReallyReallyReallyReallyReallyReallyLongQuery), Soft, Sweet | Contrary to popular belief, most apes prefer mangoes.

DO NOT DO THIS
```

Nevertheless, use of link reference definition can be used in table to prevent
long and complex table.

```markdown
Fruit | Attribute | Notes
--- | --- | --- | ---
Apple | [Juicy][juicy], Firm, Sweet | Apples keep doctors away.
Banana | [Convenient][convenient], Soft, Sweet | Contrary to popular belief, most apes prefer mangoes.

You can do this but avoid it.

[juicy]: https://example.com/SomeReallyReallyReallyReallyReallyReallyReallyReallyLongQuery
[convenient]: https://example.com/SomeDifferentReallyReallyReallyReallyReallyReallyReallyReallyLongQuery
```

Lists and subheadings usually suffice to present the same information in a
slightly less compact, though much more edit-friendly way:

```markdown
## Fruits

### Apple

* [Juicy](https://SomeReallyReallyReallyReallyReallyReallyReallyReallyReallyReallyReallyReallyReallyReallyReallyReallyLongURL)
* Firm
* Sweet

Apples keep doctors away.

### Banana

* [Convenient](https://example.com/SomeDifferentReallyReallyReallyReallyReallyReallyReallyReallyLongQuery)
* Soft
* Sweet

Contrary to popular belief, most apes prefer mangoes.
```

However, there are times when a small table is called for:

```markdown
Transport | Favored by | Advantages
--- | --- | ---
Swallow | Coconuts | Otherwise unladen
Bicycle | Miss Gulch | Weatherproof
X-34 landspeeder | Whiny farmboys | Cheap since the X-38 came out
```

Finally, sometimes information in table, even complex, is more readable once
rendered such as the tables in the [home page of this
documentation][home_page][^1].

[home_page]: /index.html

## Strongly prefer Markdown to HTML

Please prefer standard Markdown syntax wherever possible and avoid HTML hacks.
If you can’t seem to accomplish what you want, reconsider whether you really
need it. Except for big tables, Markdown meets almost all needs already.

Every bit of HTML or Javascript hacking reduces the readability and portability.
This in turn limits the usefulness of integrations with other tools, which may
either present the source as plain text or render it. See [Philosophy][philosophy].

[philosophy]: philosophy.md

## Markdown Extensions

Last word about writing documentation with markdown. If the markdown files are
used to render a documentation with [mkdocs][mkdocs], multiple markdown
extensions have been installed et configured (through `mkdocs.yml` and with the
theme [mkdocs-material][mkdocs_material]) which can be used.

These extensions allow you to enrich you render markdown such as :

  * [Admonition][mkdocs_admonition_plugin]:

    Admonition is an extension
    included in the standard Markdown library that makes it possible to add
    block-styled side content to your documentation, e.g. summaries, notes,
    hints or warnings.

  * [Footnotes][mkdocs_footnotes_plugin]:

    Footnotes is another extension
    included in the standard Markdown library. As the name says, it adds the
    ability to add inline footnotes to your documentation.

  * [Metadata][mkdocs_metadata_plugin]:

    Metadata is an extension included in
    the standard Markdown library that makes it possible to control certain
    properties in a page-specific context, e.g. the page title or
    description.

  * [Permalinks][mkdocs_permalink_plugin]:

    Permalinks are a feature of the
    Table of Contents extension, which is part of the standard Markdown
    library.

  * [PyMdown][mkdocs_pymdown_plugin]:

    PyMdown Extensions is a collection of
    Markdown extensions that add some great missing features to the standard
    Markdown library.

  * [Mermaid][mkdocs_mermaid_plugin]:

    Mermaid is a tool that generates
    diagrams and charts, from markdown-inspired text definitions

And many others.

[mkdocs_admonition_plugin]: https://squidfunk.github.io/mkdocs-material/extensions/admonition/
[mkdocs_codehilite_plugin]: https://squidfunk.github.io/mkdocs-material/extensions/codehilite/
[mkdocs_footnotes_plugin]: https://squidfunk.github.io/mkdocs-material/extensions/footnotes/
[mkdocs_metadata_plugin]: https://squidfunk.github.io/mkdocs-material/extensions/metadata/
[mkdocs_permalink_plugin]: https://squidfunk.github.io/mkdocs-material/extensions/permalinks/
[mkdocs_pymdown_plugin]: https://squidfunk.github.io/mkdocs-material/extensions/pymdown/
[mkdocs_mermaid_plugin]: https://mermaid-js.github.io/mermaid/#/flowchart
[mkdocs_material]: https://squidfunk.github.io/mkdocs-material/

[mkdocs]: https://www.mkdocs.org/

[^1]: Note that such table source are in fact automatically generated using
  jinja2 :smile:.

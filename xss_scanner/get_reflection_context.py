from lxml import html

def detect_context(search, page_html):
    page_html_tree = html.fromstring(page_html)

    result = {}
    result['payload'] = search
    result['contexts'] = []

    # node with search string
    nn_xpath = '//' + search
    nn = page_html_tree.xpath(nn_xpath)
    nn_count = len(nn)

    if nn_count:
        context = {}
        context['type'] = 'nodename'
        context['count'] = nn_count
        result['contexts'].append(context)

    # attribute name //*[ . = "val"]
    an_xpath = '//*[@' + search + ']'
    an = page_html_tree.xpath(an_xpath)
    an_count = len(an)

    if an_count:
        context = {}
        context['type'] = 'attributename'
        context['count'] = an_count
        result['contexts'].append(context)

    # attribute value
    av_xpath = '//*[@*[contains(.,\'' + search + '\')]]'
    av = page_html_tree.xpath(av_xpath)
    av_count = len(av)

    if av_count:
        context = {}
        context['type'] = 'attributevalue'
        context['count'] = av_count
        result['contexts'].append(context)

    # text value
    tv_xpath = '//*[contains(text(),\'' + search + '\')]'
    tv = page_html_tree.xpath(tv_xpath)
    tv_count = len(tv)

    if tv_count:
        context = {}
        context['type'] = 'text'
        context['count'] = tv_count
        result['contexts'].append(context)

    # html comment
    com_xpath = '//*[comment()[contains(.,\'' + search + '\')]]'
    com = page_html_tree.xpath(com_xpath)
    com_count = len(com)

    if com_count:
        context = {}
        context['type'] = 'comment'
        context['count'] = com_count
        result['contexts'].append(context)

    # ** Special instances of the above... **

    # <style>
    style_xpath = '//style[contains(text(),\'' + search + '\')]'
    style = page_html_tree.xpath(style_xpath)
    style_count = len(style)

    if style_count:
        context = {}
        context['type'] = 'style'
        context['count'] = style_count
        result['contexts'].append(context)

    # inside id attribute value
    idattrib_xpath = '//*[@id[contains(.,\'' + search + '\')]]'
    idattrib = page_html_tree.xpath(idattrib_xpath)
    idattrib_count = len(idattrib)

    if idattrib_count:
        context = {}
        context['type'] = 'idattrib'
        context['count'] = idattrib_count
        result['contexts'].append(context)

    # inside class attribute value
    clazz_xpath = '//*[@class[contains(.,\'' + search + '\')]]'
    clazz = page_html_tree.xpath(clazz_xpath)
    clazz_count = len(clazz)

    if clazz_count:
        context = {}
        context['type'] = 'classattrib'
        context['count'] = clazz_count
        result['contexts'].append(context)

    # inside style attribute value
    styleattrib_xpath = '//*[@style[contains(.,\'' + search + '\')]]'
    styleattrib = page_html_tree.xpath(styleattrib_xpath)
    styleattrib_count = len(styleattrib)

    if styleattrib_count:
        context = {}
        context['type'] = 'styleattrib'
        context['count'] = styleattrib_count
        result['contexts'].append(context)

    # ** Harder ones... Javascript **

    # inside <script> header
    jsnode_xpath = '//script[contains(text(),\'' + search + '\')]'
    jsnode = page_html_tree.xpath(jsnode_xpath)
    jsnode_count = len(jsnode)

    if jsnode_count:
        context = {}
        context['type'] = 'jsnode'
        context['count'] = jsnode_count
        result['contexts'].append(context)

    # each instance of <script> comes out differently, parse each for content

    jssqcount = 0
    jsdqcount = 0
    js_xpath = '//script[contains(text(),\'' + search + '\')]'
    js = page_html_tree.xpath(js_xpath)

    for js_finding in js:
        js_string = js_finding.text

        # TODO below line is a mix of Javascript and Python, implement for some rare cases...
        #escaped_search = search.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')

        sqre = re.compile('\'(?:[^\'\\\\]|\\\\.)*' + search + '(?:[^\'\\\\]|\\\\.)*\'')
        #sqre = re.compile('\'(?:[^\'\\\\]|\\\\.)*' + escaped_search + '(?:[^\'\\\\]|\\\\.)*\'')
        dqre = re.compile('"(?:[^"\\\\]|\\\\.)*' + search + '(?:[^"\\\\]|\\\\.)*"')
        #dqre = re.compile('(?:[^"\\\\]|\\\\.)*' + escaped_search + '(?:[^"\\\\]|\\\\.)*"')

        sq = sqre.findall(js_string)
        dq = dqre.findall(js_string)

        jssqcount += len(sq)
        jsdqcount += len(dq)

    if jssqcount:
        context = {}
        context['type'] = 'jssinglequote'
        context['count'] = jssqcount
        result['contexts'].append(context)

    if jsdqcount:
        context = {}
        context['type'] = 'jsdoublequote'
        context['count'] = jsdqcount
        result['contexts'].append(context)

    # inside any onXXXX() attribute
    onattrib_xpath = '//*[@onerror[contains(.,\'' + search \
            + '\')] or @onload[contains(.,\'' + search \
            + '\')] or @onclick[contains(.,\'' + search \
            + '\')] or @oncontextmenu[contains(.,\'' + search \
            + '\')] or @ondblclick[contains(.,\'' + search \
            + '\')] or @onmousedown[contains(.,\'' + search \
            + '\')] or @onmouseenter[contains(.,\'' + search \
            + '\')] or @onmouseleave[contains(.,\'' + search \
            + '\')] or @onmousemove[contains(.,\'' + search \
            + '\')] or @onmouseover[contains(.,\'' + search \
            + '\')] or @onmouseout[contains(.,\'' + search \
            + '\')] or @onmouseup[contains(.,\'' + search \
            + '\')] or @onkeydown[contains(.,\'' + search \
            + '\')] or @onkeypress[contains(.,\'' + search \
            + '\')] or @onkeyup[contains(.,\'' + search \
            + '\')] or @onabort[contains(.,\'' + search \
            + '\')] or @onbeforeunload[contains(.,\'' + search \
            + '\')] or @onhashchange[contains(.,\'' + search \
            + '\')] or @onpageshow[contains(.,\'' + search \
            + '\')] or @onpagehide[contains(.,\'' + search \
            + '\')] or @onresize[contains(.,\'' + search \
            + '\')] or @onscroll[contains(.,\'' + search \
            + '\')] or @onunload[contains(.,\'' + search \
            + '\')] or @onblur[contains(.,\'' + search \
            + '\')] or @onchange[contains(.,\'' + search \
            + '\')] or @onfocus[contains(.,\'' + search \
            + '\')] or @onfocusin[contains(.,\'' + search \
            + '\')] or @onfocusout[contains(.,\'' + search \
            + '\')] or @oninput[contains(.,\'' + search \
            + '\')] or @oninvalid[contains(.,\'' + search \
            + '\')] or @onreset[contains(.,\'' + search \
            + '\')] or @onsearch[contains(.,\'' + search \
            + '\')] or @onselect[contains(.,\'' + search \
            + '\')] or @ondrag[contains(.,\'' + search \
            + '\')] or @ondragend[contains(.,\'' + search \
            + '\')] or @ondragenter[contains(.,\'' + search \
            + '\')] or @ondragleave[contains(.,\'' + search \
            + '\')] or @ondragover[contains(.,\'' + search \
            + '\')] or @ondragstart[contains(.,\'' + search \
            + '\')] or @ondrop[contains(.,\'' + search \
            + '\')] or @oncopy[contains(.,\'' + search \
            + '\')] or @oncut[contains(.,\'' + search \
            + '\')] or @onpaste[contains(.,\'' + search \
            + '\')] or @onafterprint[contains(.,\'' + search \
            + '\')] or @onbeforeprint[contains(.,\'' + search \
            + '\')] or @onabort[contains(.,\'' + search \
            + '\')] or @oncanplay[contains(.,\'' + search \
            + '\')] or @oncanplaythrough[contains(.,\'' + search \
            + '\')] or @ondurationchange[contains(.,\'' + search \
            + '\')] or @onemptied[contains(.,\'' + search \
            + '\')] or @onended[contains(.,\'' + search \
            + '\')] or @onloadeddata[contains(.,\'' + search \
            + '\')] or @onloadedmetadata[contains(.,\'' + search \
            + '\')] or @onloadstart[contains(.,\'' + search \
            + '\')] or @onpause[contains(.,\'' + search \
            + '\')] or @onplay[contains(.,\'' + search \
            + '\')] or @onplaying[contains(.,\'' + search \
            + '\')] or @onprogress[contains(.,\'' + search \
            + '\')] or @onratechange[contains(.,\'' + search \
            + '\')] or @onseeked[contains(.,\'' + search \
            + '\')] or @onseeking[contains(.,\'' + search \
            + '\')] or @onstalled[contains(.,\'' + search \
            + '\')] or @onsuspend[contains(.,\'' + search \
            + '\')] or @ontimeupdate[contains(.,\'' + search \
            + '\')] or @onvolumechange[contains(.,\'' + search \
            + '\')] or @onwaiting[contains(.,\'' + search \
            + '\')] or @onopen[contains(.,\'' + search \
            + '\')] or @onmessage[contains(.,\'' + search \
            + '\')] or @onmousewheel[contains(.,\'' + search \
            + '\')] or @ononline[contains(.,\'' + search \
            + '\')] or @onoffline[contains(.,\'' + search \
            + '\')] or @onpopstate[contains(.,\'' + search \
            + '\')] or @onshow[contains(.,\'' + search \
            + '\')] or @onstorage[contains(.,\'' + search \
            + '\')] or @ontoggle[contains(.,\'' + search \
            + '\')] or @onwheel[contains(.,\'' + search \
            + '\')] or @ontouchcancel[contains(.,\'' + search \
            + '\')] or @ontouchend[contains(.,\'' + search \
            + '\')] or @ontouchmove[contains(.,\'' + search \
            + '\')] or @ontouchstart[contains(.,\'' + search \
            + '\')] or @onsubmit[contains(.,\'' + search + '\')]]'
    onattrib = page_html_tree.xpath(onattrib_xpath)
    onattrib_count = len(onattrib)

    if onattrib_count:
        context = {}
        context['type'] = 'onattrib'
        context['count'] = onattrib_count
        result['contexts'].append(context)

     # JS errors
    ''' error_count = 0
    for error_popup in rendered_page_output['page_errors']:
        if search in error_popup:
            error_count += 1

    if error_count:
        context = {}
        context['type'] = 'js_error'
        context['count'] = error_count
        result['contexts'].append(context)

    # JS console messages
    console_msg_count = 0
    for console_msg in rendered_page_output['page_console_messages']:
        if search in console_msg:
            console_msg_count += 1

    if console_msg_count:
        context = {}
        context['type'] = 'js_console'
        context['count'] = console_msg_count
        result['contexts'].append(context)

    # prompt() popups
    prompt_popup_count = 0
    for prompt_popup in rendered_page_output['page_prompts']:
        if search in prompt_popup:
            prompt_popup_count += 1

    if prompt_popup_count:
        context = {}
        context['type'] = 'js_prompt'
        context['count'] = prompt_popup_count
        result['contexts'].append(context)

    # confirm() popups
    confirm_popup_count = 0
    for confirm_popup in rendered_page_output['page_confirms']:
        if search in confirm_popup:
            confirm_popup_count += 1

    if confirm_popup_count:
        context = {}
        context['type'] = 'js_confirm'
        context['count'] = confirm_popup_count
        result['contexts'].append(context) '''

    return result
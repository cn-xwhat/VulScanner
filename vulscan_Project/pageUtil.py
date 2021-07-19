import re


def get_pages(page, last_page):
    page_list = []
    if last_page < 9:
        for i in range(1, last_page + 1):
            page_list.append(i)
        return page_list
    if page < 7:
        for i in range(1, 9):
            page_list.append(i)
        page_list.extend(["...", last_page - 1, last_page])
    elif page < last_page - 4:
        page_list.extend([1, 2, "..."])
        for i in range(-3, 3):
            page_list.append(page + i)
        page_list.extend(["...", last_page - 1, last_page])
    else:
        page_list.extend([1, 2, "..."])
        for i in range(last_page - 7, last_page + 1):
            page_list.append(i)
    return page_list

def get_lastpage(count, each_num):
    if count == 0:
        return 1
    if count % each_num == 0:
        return int(count / each_num)
    else:
        return int(count / each_num) + 1

def get_ctx(ctx, list_name, all_list, page, last_page, query, base_path):
    ctx[list_name] = all_list  # 本页显示总列表
    ctx["count"] = len(all_list)
    ctx["page"] = page  # 当前页数
    ctx['notfirst'] = 0 if page == 1 else -1
    ctx['notlast'] = 0 if page == last_page else 1
    ctx['pages'] = get_pages(page, last_page)
    ctx["query"] = query
    base_path = re.sub(r"((\?)?(&)?page=\w*)", "", base_path)
    ctx["page_url"] = base_path + ("&page=" if "?" in base_path else "?page=")
    return ctx
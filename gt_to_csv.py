import pdfplumber
import os
import numpy as np


def keep_visible_lines(obj):
    if obj['object_type'] == 'rect':
        # print(obj['non_stroking_color'])
        return obj['non_stroking_color'] == (0, 0, 0) or obj['non_stroking_color'] == (0,)
    return True


def convert(pdf, skip_first_page=False, mode="I"):
    newtable = []

    if mode == "I":
        page = pdf.pages[0].filter(keep_visible_lines)
        im = page.to_image()
        im = im.debug_tablefinder(tf={"vertical_strategy": "explicit",
                                      "horizontal_strategy": "explicit",
                                      "explicit_vertical_lines": page.curves+page.edges,
                                      "explicit_horizontal_lines": page.curves+page.edges,
                                      "intersection_tolerance": 15})
        im.save("test.png")
        table = page.extract_tables(table_settings={"vertical_strategy": "explicit",
                                                    "horizontal_strategy": "explicit",
                                                    "explicit_vertical_lines": page.curves+page.edges,
                                                    "explicit_horizontal_lines": page.curves+page.edges,
                                                    })[0]

        for row in table:
            counter = 0
            if "" in row or None in row or len(row) < 6 or row == ['Option', 'Combination of components', 'A*', 'A', 'B', 'C', 'D', 'E']:
                pass
            else:
                newrow = []
                for item in row:
                    if counter == 1:
                        newrow.append(item.replace(", ", "/"))
                    else:
                        newrow.append(item)
                    counter += 1

                newtable.append(newrow)

        return newtable

    if mode != "I":
        page_counter = 0

        for page in pdf.pages:
            if skip_first_page == True and page_counter == 0:
                page_counter += 1
                continue

            page = page.filter(keep_visible_lines)
            im = page.to_image()

            if len(page.edges) == 0:
                continue

            table = page.extract_tables(table_settings={"vertical_strategy": "explicit",
                                                        "horizontal_strategy": "explicit",
                                                        "explicit_vertical_lines": page.curves+page.edges,
                                                        "explicit_horizontal_lines": page.curves+page.edges,
                                                        "intersection_tolerance": 15, })[-1]

            for row in table:
                counter = 0
                # I AM TOO LAZY TO MAKE THIS SMARTER BUT IT GOT THE JOB DONE AND ITS TEMPORARY
                if "components" in row or "" in row or None in row or len(row) < 6 or row == ['Option', 'Combination of components', 'A*', 'A', 'B', 'C', 'D', 'E'] or row == ['Option', 'Combination of\nComponents', 'A*', 'A', 'B', 'C', 'D', 'E'] or row == ['Option', 'Maximum mark after weighting', 'Combination of\ncomponents', 'A*', 'A', 'B', 'C', 'D', 'E']:
                    pass
                else:
                    newrow = []
                    for item in row:
                        if "Option" in item or "mark" in item or "components" in item or item == "":
                            break
                        if counter == 1:
                            newrow.append(item.replace(
                                "\n", " ").replace(", ", "/"))
                        else:
                            newrow.append(item)
                        counter += 1

                    newtable.append(newrow)

        return newtable


CODE = 9709

for file in os.listdir(fr"dir\data\{CODE}"):
    filename = os.fsdecode(file)

    if filename.endswith(".pdf"):
        pdf = pdfplumber.open(
            fr"dir\data\{CODE}\{filename}")

        print(filename)
        os.makedirs(
            f"dir\\data\\{CODE}-Converted\\", exist_ok=True)

        if "_m" not in filename:
            newtable = list(filter(None, convert(
                pdf, mode="j", skip_first_page=True)))

        else:
            newtable = list(filter(None, convert(
                pdf, mode="j")))

        print(newtable)

        np.savetxt(
            f"data\{CODE}-Converted\{filename[:-4]}.csv", newtable, delimiter=", ", encoding="UTF-8", fmt="% s")

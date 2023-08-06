from ums import User


def main():

    TEST = False
    if TEST:
        print("Test Started . . .")
        user = User(registration="11917210", password="Yeahhia@1236#")
        test_dict_function = {
            "announcement": user.annoucements(),
            "messages": user.annoucements(),
            "user profile": user.user_profile(),
            "datesheet": user.datesheet(),
            "grades": user.grades(),
            "Marks": user.marks(),
            "classes": user.classes()
        }
        for k, v in test_dict_function.items():
            p = "Fail"
            e = v
            if "error" not in v.keys():
                p = "Pass"
                e = ""
            else:
                e = v["error"]
            text = f"{k} {' '*(15-len(k))}-- [ {p} ]" + ("" if e == "" else f"( {e} )")
            print(text)
    else:
        pass


if __name__ == '__main__':
    main()

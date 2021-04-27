import yaml

def recurse(obj, path=""):
    items = []
    for key in obj:
        if key != "items":
            new_path = ""
            if path == "":
                new_path = key
            else:
                new_path = path + "." + key

            splitted = new_path.split(".")
            name = splitted[len(splitted) - 1]

            new_obj = {"uid": new_path, "name": name, "items": obj[key].get("items") or []}
            new_obj["items"].append(recurse(obj[key], new_path))
            items.append(new_obj)
    return items

# Start of script

toc = yaml.load(open("./api/toc.yml", "r").read(), Loader=yaml.SafeLoader)
namespaces = {}

for line in toc:
    full_namespace = line["uid"]
    split_namespace = full_namespace.split(".")

    parent = namespaces

    for word in split_namespace:
        partial_namespace = word

        if not parent.get(partial_namespace):
            parent[partial_namespace] = {}
        parent = parent[partial_namespace]

    if not parent.get("items"):
        parent["items"] = line["items"]
    else:
        parent["items"].append(line)

new_toc = []
items = recurse(namespaces)

open("./api/toc.yml", "a").write(yaml.dump(items))

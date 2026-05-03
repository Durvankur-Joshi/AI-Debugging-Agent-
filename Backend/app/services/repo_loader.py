import os

def load_repo_files(repo_path: str):
    code_files = []

    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith((".py", ".js", ".ts", ".jsx", ".tsx")):
                full_path = os.path.join(root, file)

                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        content = f.read()

                        code_files.append({
                            "path": full_path,
                            "content": content
                        })
                except Exception as e:
                    print("Error reading file:", full_path, e)

    return code_files
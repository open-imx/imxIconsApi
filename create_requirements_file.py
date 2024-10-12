import tomllib  # note that this is a 3.11 function and will fail on py 3.10 and below!


def extract_project_dependencies(pyproject_path):
    with open(pyproject_path, 'rb') as file:
        data = tomllib.load(file)

    dependencies = data.get('project', {}).get('dependencies', [])
    return [dep.strip().strip('"').strip("'") for dep in dependencies]


def write_requirements_file(dependencies, file_path):
    with open(file_path, 'w') as file:
        for dep in dependencies:
            file.write(dep + '\n')


def main():
    pyproject_path = 'pyproject.toml'
    requirements_path = 'requirements.txt'

    dependencies = extract_project_dependencies(pyproject_path)
    write_requirements_file(dependencies, requirements_path)


if __name__ == '__main__':
    main()

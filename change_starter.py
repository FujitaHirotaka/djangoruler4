import os
import shutil
import json
import copy

#グローバル変数の設定
project_file_set = {"settings.py", "urls.py", "wsgi.py"}
project_file_list = list(project_file_set)
app_file_set = {"admin.py", "views.py", "tests.py", "models.py"}
app_file_list = list(app_file_set)
app_file_list.append("forms.py")
template_file_set={"base.html","index.html"}
static_folder_set={"bootstrap","jquery"}
template_folder_list = ["project", "app", "templates", "static"]
template_folder_path = "C:/Users/fujita/PycharmProjects/filetemplate" #これについては使用環境ごとに変える必要がある
path_dict = {}
templatefile_path_dict = {}
base_dir = os.path.dirname(os.path.abspath(__file__))


def get_app_and_project_names():
    #カレントディレクトリ内にあるフォルダ名を集め、アプリ名、プロジェクト名として収集する（この段階ではアプリとプロジェクトの判別はついていない９
    files_and_directories=os.listdir(base_dir)
    apps_and_project=[i for i in files_and_directories if os.path.isdir(os.path.join(base_dir, i))]
    if "static" in apps_and_project: #"staticフォルダはdjangoの構造上manage.pyと同階層に作ったが、これはアプリでもプロジェクトでもないため"
        apps_and_project.remove("static")
    return apps_and_project

def make_dict_of_app_and_project(app_and_project_list):
    #アプリ名とプロジェクト名を判別し、辞書として格納。{"アプリ名":"A","プロジェクト名":"P"}}
    app_and_project_dict={}
    for i in app_and_project_list:
        if not (project_file_set-set(os.listdir(os.path.join(base_dir, i)))):
            app_and_project_dict[i]="project" #P:projectの略
        if not (app_file_set-set(os.listdir(os.path.join(base_dir, i)))):
            app_and_project_dict[i]="app" #A:Appの略
    return app_and_project_dict

def confirm_folder_existence(path):
    #指定したpathにフォルダがあるかどうかを調べる。なければ例外処理。
    if not os.path.exists(path):
        raise Exception(path+"というフォルダがないようだ")

def confirm_files_of_app_and_project_in_filetemplate():
    # filepathの中にproject、app、フォルダがきちんとあるかどうかをチェック。
    if (project_file_set-set(os.listdir(os.path.join(template_folder_path, "project")))):
            raise Exception(os.path.join(template_folder_path, "project")+"でファイルが足りないようだ")
    if (app_file_set-set(os.listdir(os.path.join(template_folder_path, "app")))):
            raise Exception(os.path.join(template_folder_path, "app")+"でファイルが足りないようだ")
    if (static_folder_set - set(os.listdir(os.path.join(template_folder_path, "static")))):
            raise Exception(os.path.join(template_folder_path, "static") + "でファイルが足りないようだ")
    if (template_file_set - set(os.listdir(os.path.join(template_folder_path, "templates")))):
            raise Exception(os.path.join(template_folder_path, "templates") + "でファイルが足りないようだ")


def function_decorator(func):
        def wrapper(*args, **kwargs):
            shutil.copy(templatefile_path_dict[file_name], path_dict[file_name])
            with open(path_dict[file_name], 'r') as f:
                        sentence_list=f.readlines()
                        sentence_dict=dict(zip(sentence_list, list(range(len(sentence_list)))))
                        sentence_list=func(sentence_list, sentence_dict)
            with open(path_dict[file_name], 'w') as f:
                        f.writelines(sentence_list)
        return wrapper

@function_decorator
def add_new_apps_to_INSTALLED_APPS_in_settings_py( sentence_list, sentence_dict):
    aaa = ["ROOT_URLCONF = 'project.urls'\n", "WSGI_APPLICATION = 'project.wsgi.application'\n"]
    sentence_list=list(sentence_list)
    for iii in aaa:
        sentence_list[sentence_dict[iii]] = iii.replace("project", project_name)
    for ii in app_and_project_dict.keys():
        if app_and_project_dict[ii] == "app":
            sentence_list.insert(sentence_dict["    'django.contrib.staticfiles',\n"] + 1, "    '" + ii + "',\n")
    return sentence_list

@function_decorator
def add_path_to_urls_py_in_project_dir(sentence_list, sentence_dict):
    for ii in app_and_project_dict.keys():
        if app_and_project_dict[ii] == "app":
            sentence_list.insert(sentence_dict["    path('admin/', admin.site.urls),\n"] + 1,
                                 ("    path('" + ii + "/', include('" + ii + ".urls')),\n"))
    return sentence_list

@function_decorator
def change_templatefilepath_in_views_py(sentence_list, sentence_dict):
    sentence = "    return render(request, 'apri1/index.html', {})\n"
    sentence_list[sentence_dict[sentence]] = sentence.replace("apri1", app_name)
    return sentence_list

@function_decorator
def add_path_to_urls_py_in_app_dir(sentence_list, sentence_dict):
    sentence_list.insert(sentence_dict["urlpatterns = [\n"], ("app_name='" + app_name + "'\n"))
    return sentence_list

def copy_templates_of_static_in_project():
        if not os.path.exists(os.path.join(base_dir, "static")):
            os.mkdir(os.path.join(base_dir, "static"))
            for ii in os.listdir(os.path.join(template_folder_path, "static")):
                shutil.copytree(os.path.join(template_folder_path, "static", ii), os.path.join(base_dir, "static", ii))

def copy_templates_of_templates_and_static_to_each_app():
        #アプリ関係のファイルの処理
            for ii in ["templates", "static"]:
                #各アプリにtemplatesとstaticのフォルダ構造を作る(app/templates/appやapp/static/app)
                if not os.path.exists(os.path.join(base_dir, app_name, ii)):
                    os.mkdir(os.path.join(base_dir, app_name, ii))
                if not os.path.exists(os.path.join(base_dir, app_name, ii,app_name)):
                    os.mkdir(os.path.join(base_dir, app_name, ii,app_name))
                if ii=="templates":
                        for iii in os.listdir(os.path.join(template_folder_path, "templates")):
                        # 各アプリのtemplatesにbase.htmlやindex.htmlを作る
                            shutil.copy(os.path.join(template_folder_path,"templates",iii),
                                    os.path.join(base_dir,app_name,"templates", app_name,iii))

@function_decorator
def bind_index_html_to_base_html(sentence_list, sentence_dict):
                sentence_list.insert(1, ("{% extends '"+app_name+"/base.html' %}\n"))
                return sentence_list

def write_already_treated_apps_and_project_in_json_format():
    with open("already_treated_apps_and_project.json", "w") as f:
            json.dump(app_and_project_dict, f)

def read_already_treated_apps_and_project_in_json_format():
    try:
        with open("already_treated_apps_and_project.json", "r") as f:
                app_and_project_dict_yet = json.load(f)
        return app_and_project_dict_yet
    except:
        return {}


if __name__=="__main__":

    app_and_project_list=get_app_and_project_names()
    app_and_project_dict=make_dict_of_app_and_project(app_and_project_list)

    app_and_project_dict_yet=read_already_treated_apps_and_project_in_json_format()
    app_and_project_dict_new=copy.deepcopy(app_and_project_dict)
    for i in app_and_project_dict_yet.keys():
        del app_and_project_dict_new[i]


    for i in template_folder_list:
        confirm_folder_existence(os.path.join(template_folder_path, i))

    confirm_files_of_app_and_project_in_filetemplate()


    for i in app_and_project_dict.keys():
         if app_and_project_dict[i] == "project":
             project_name = i
             app_or_project_or_template_or_static="project"


    for i in ["settings.py","urls.py"]:
        file_name =i
        path_dict[i]=os.path.join(base_dir, project_name, i)
        templatefile_path_dict[i]=os.path.join(template_folder_path, app_or_project_or_template_or_static, i)
        if i=="settings.py":
                 add_new_apps_to_INSTALLED_APPS_in_settings_py()
        elif i=="urls.py":
                 add_path_to_urls_py_in_project_dir()

    copy_templates_of_static_in_project()


    for i in app_and_project_dict_new.keys():
        if app_and_project_dict_new[i]=="app":
            app_name = i
            app_or_project_or_template_or_static = "app"

            for ii in ["views.py", "urls.py"]:
                file_name =ii
                path_dict[ii]=os.path.join(base_dir, app_name, ii)
                templatefile_path_dict[ii]=os.path.join(template_folder_path, app_or_project_or_template_or_static,ii)
                if ii=="views.py":
                    change_templatefilepath_in_views_py()
                elif ii == "urls.py":
                    add_path_to_urls_py_in_app_dir()
            copy_templates_of_templates_and_static_to_each_app()

            file_name="index.html"
            templatefile_path_dict["index.html"] = os.path.join(template_folder_path, "templates", "index.html")
            path_dict["index.html"] = os.path.join(base_dir, app_name, "templates", app_name, "index.html")
            bind_index_html_to_base_html()

    write_already_treated_apps_and_project_in_json_format()

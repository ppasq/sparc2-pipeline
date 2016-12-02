import os
import yaml

from pythoncliutil.utils import request_input, request_continue

from fabric.api import env, sudo, run, cd, local, put, task, get
from fabric.utils import abort

from enumerations import DB_OPERATIONS, GEOMETRY_TYPES, DB_TABLE_SEPARATORS


#############################################################
# The Public API
@task
def dev(*args):

    env_config = yaml.load(file("env/dev.yml", 'r'))
    print "Loaded environment from env/dev.yml"
    env.disable_known_hosts = env_config["disable_known_hosts"] if env_config["disable_known_hosts"] else False  # noqa
    env.user = env_config["user"]
    env.group = env_config["group"]
    env.port = env_config["user"]
    env.password = env_config["password"] if env_config["password"] else None
    env.hosts = env_config["hosts"]
    env.key_filename = os.path.expanduser(env_config["key_filename"]) if env_config["key_filename"] else None  # noqa
    env["sparc2_venv"] = env_config["sparc2"]["venv"]
    env["sparc2_user"] = env_config["sparc2"]["user"]
    env["sparc2_db_user"] = env_config["sparc2"]["db"]["user"]
    env["sparc2_db_password"] = env_config["sparc2"]["db"]["password"]
    env["sparc2_db_name"] = env_config["sparc2"]["db"]["name"]
    env.sparc2_connstr = "host={host} user={user} dbname={dbname} password={password}".format(** {
        "host": env_config["sparc2"]["db"]["host"],
        "dbname": env_config["sparc2"]["db"]["name"],
        "user": env_config["sparc2"]["db"]["user"],
        "password": env_config["sparc2"]["db"]["password"]
    })


@task
def prod(*args):
    env_config = yaml.load(file("env/prod.yml", 'r'))
    print "Loaded environment from env/prod.yml"
    env.disable_known_hosts = env_config["disable_known_hosts"] if env_config["disable_known_hosts"] else False
    env.user = env_config["user"]
    env.group = env_config["group"]
    env.port = env_config["user"]
    env.password = env_config["password"] if env_config["password"] else None
    env.hosts = env_config["hosts"]
    env.key_filename = os.path.expanduser(env_config["key_filename"]) if env_config["key_filename"] else None
    env["sparc2_venv"] = env_config["sparc2"]["venv"]
    env["sparc2_user"] = env_config["sparc2"]["user"]
    env["sparc2_db_user"] = env_config["sparc2"]["db"]["user"]
    env["sparc2_db_password"] = env_config["sparc2"]["db"]["password"]
    env["sparc2_db_name"] = env_config["sparc2"]["db"]["name"]
    env.sparc2_connstr = "host={host} user={user} dbname={dbname} password={password}".format(** {
        "host": env_config["sparc2"]["db"]["host"],
        "dbname": env_config["sparc2"]["db"]["name"],
        "user": env_config["sparc2"]["db"]["user"],
        "password": env_config["sparc2"]["db"]["password"]
    })


@task
def host_type(*args):

    if "hosts" not in env or not env.hosts:
        abort("Hosts not specified.  Did you load your environment first?")

    return _host_type(*args)


@task
def lsb_release(*args):

    if "hosts" not in env or not env.hosts:
        abort("Hosts not specified.  Did you load your environment first?")

    return _lsb_release(*args)


@task
def cp(** kwargs):
    _pipeline_copy(** kwargs)


@task
def copy(** kwargs):
    _pipeline_copy(** kwargs)


@task
def pipeline_copy(** kwargs):
    """
    Execute local files on SPARC database

    Puts via SFTP local files into the remote's "drop" folder

    Options:
    src = local file path
    dest = remote destination folder
    """

    if "hosts" not in env or not env.hosts:
        abort("Hosts not specified.  Did you load your environment first?")

    return _pipeline_copy(** kwargs)


@task
def shp(** kwargs):
    import_shapefile(**kwargs)


@task
def import_shapefile(** kwargs):
    """
    Import local shapefile into a SPARC instance

    Puts via SFTP local files into the remote's "drop" folder and then
    runs ogr2ogr to import all of them.

    Options:
    local_path = local file path
    drop = temporary drop folder

    table = the database table name
    geometry_type = the geometry type (POINT, LINESTRING, MULTIPOLYGON)
    operation = operation to perform (append, replace)
    """

    if "hosts" not in env or not env.hosts:
        abort("Hosts not specified.  Did you load your environment first?")

    return _pipeline_import_shapefile(** kwargs)


@task
def import_tables(**kwargs):
    """
    Import local file into the SPARC instance

    Puts via SFTP local files into the remote's "drop" folder and then
    runs SQL 'COPY' command to import all of them.

    Options:
    local_path = local file path
    drop = temporary drop folder

    table = the database table name
    operation = operation to perform (append, replace)
    """

    if "hosts" not in env or not env.hosts:
        abort("Hosts not specified.  Did you load your environment first?")

    return _pipeline_import_tables(**kwargs)


@task
def export_shapefiles(**kwargs):
    """
    Export table from SPARC Interface to local shapefile

    Runs ogr2ogr to export table to shapefile in the
    the remote's "drop" folder and then gets via SFTP.

    Options:
    local_path = local file path
    drop = temporary drop folder

    table = the database table name
    geometry_type = the geometry type (POINT, LINESTRING, MULTIPOLYGON)
    operation = operation to perform (append, replace)
    """

    if "hosts" not in env or not env.hosts:
        abort("Hosts not specified.  Did you load your environment first?")

    return _pipeline_export_shapefiles(**kwargs)


@task
def export_tables(**kwargs):
    """
    Export table from SPARC Interface to local shapefile

    Runs ogr2ogr to export table to shapefile in the
    the remote's "drop" folder and then gets via SFTP.

    Options:
    local_path = local file path
    drop = temporary drop folder

    table = the database table name
    operation = operation to perform (append, replace)
    """

    if "hosts" not in env or not env.hosts:
        abort("Hosts not specified.  Did you load your environment first?")

    return _pipeline_export_tables(**kwargs)


@task
def sql(** kwargs):
    pipeline_exec_sql(** kwargs)


@task
def pipeline_exec_sql(** kwargs):
    """
    Execute local SQL file on SPARC database

    Puts via SFTP local SQL files into the remote's "drop" folder and then
    executes them on the SPARC database

    Options:
    local_path = local file path
    drop = temporary drop folder
    """

    if "hosts" not in env or not env.hosts:
        abort("Hosts not specified.  Did you load your environment first?")

    return _pipeline_exec_sql(** kwargs)


@task
def pipeline_sql_schemas(** kwargs):
    """
    Creates schemas in SPARC database

    Options:
    schemas = list of schemas
    sep = delimiter for list of schemas
    """

    if "hosts" not in env or not env.hosts:
        abort("Hosts not specified.  Did you load your environment first?")

    return _pipeline_sql_schemas(** kwargs)


@task
def pipeline_sql_clear(** kwargs):
    """
    Creates schemas in SPARC database

    Options:
    tables = list of tables
    sep = delimiter for list of tables
    """

    if "hosts" not in env or not env.hosts:
        abort("Hosts not specified.  Did you load your environment first?")

    return _pipeline_sql_clear(** kwargs)


@task
def py(** kwargs):
    pipeline_exec_python(** kwargs)


@task
def pipeline_exec_python(** kwargs):
    """
    Execute local python files on SPARC database

    Puts via SFTP local python files into the remote's "drop" folder and then
    executes them on the SPARC database

    Options:
    local_path = local file path
    drop = temporary drop folder
    chdir = cd into this directory before running the command
    """

    if "hosts" not in env or not env.hosts:
        abort("Hosts not specified.  Did you load your environment first?")

    return _pipeline_exec_python(** kwargs)


#############################################################
# The Private API

def _host_type():
    run('uname -s')


def _lsb_release():
    run('lsb_release -c')


def _pipeline_import_shapefile(**kwargs):

    local_path = request_input("Local File Path", kwargs.get("local_path", None), True)
    drop = request_input("Remote Drop Folder", kwargs.get("drop", None), True)

    table = request_input("Database Table", kwargs.get("table", None), True)
    geometry_type = request_input("Geometry Type", kwargs.get("geometry_type", None), True, options=GEOMETRY_TYPES)
    op = request_input("Operation", kwargs.get("op", None), True, options=DB_OPERATIONS)
    srid = request_input("SRID (Enter to skip)", kwargs.get("srid", None), False)

    if request_continue():
        sudo("[ -d {d} ] || mkdir -p {d}".format(d=drop))
        remote_files = put(local_path, drop, mode='0444', use_sudo=True)
        if remote_files:
            with cd(drop):
                connstr = env["sparc2_connstr"]
                for remote_file in remote_files:
                    shapefile = None
                    if remote_file.endswith(".shp"):
                        shapefile = remote_file
                    elif remote_file.endswith(".zip"):
                        sudo("unzip {f}".format(f=remote_file))
                        shapefile = remote_file[0:-4] + ".shp"

                    if shapefile:
                        flags = []
                        if op == "append":
                            flags.append("-append")
                        elif op == "replace":
                            flags.append("-preserve_fid")
                            flags.append("-overwrite")
                        if srid:
                            flags.append('-a_srs "{srid}"'.format(srid=srid))
                        cmd = 'ogr2ogr {flags} -f "PostgreSQL" PG:"{connstr}" -nln {table} -nlt {geometry_type} -lco PRECISION=FALSE \'{shapefile}\''.format(** {
                            "connstr": connstr,
                            "table": table,
                            "geometry_type": geometry_type,
                            "shapefile": shapefile,
                            "flags": " ".join(flags)
                        })
                        run(cmd)
        else:
            print "No files uploaded"
    else:
        abort("User requested abort.")


def _pipeline_import_tables(**kwargs):

    local_path = request_input("Local File Path", kwargs.get("local_path", None), True)
    drop = request_input("Remote Drop Folder", kwargs.get("drop", None), True)

    table = request_input("Database Table", kwargs.get("table", None), True)
    op = request_input("Operation", kwargs.get("op", None), True, options=DB_OPERATIONS)

    if request_continue():
        sudo("[ -d {d} ] || mkdir -p {d}".format(d=drop))
        sudo("chown {u}:{g} -R {d}".format(d=drop, u=env["user"], g=env["group"]))
        remote_files = put(local_path, drop, mode='0444', use_sudo=True)
        if remote_files:
            with cd(drop):
                for remote_file in remote_files:
                    f = None
                    delimiter = None
                    if remote_file.endswith(".csv"):
                        f = remote_file
                        delimiter = ','
                    elif remote_file.endswith(".tsv"):
                        f = remote_file
                        delimiter = '\t'
                    if f:
                        file_path = os.path.join(drop, f)
                        if op == "replace":
                            try:
                                sql = "DELETE FROM {table};".format(table=table)
                                cmd = "PGPASSWORD='{password}' psql -U {user} -d {dbname} -c \"{sql}\"".format(** {
                                    "sql": sql,
                                    "password": env["sparc2_db_password"],
                                    "user": env["sparc2_db_user"],
                                    "dbname":  env["sparc2_db_name"]
                                })
                                run(cmd)
                            except:
                                print "Tried to delete from non-existant table "+table+"."

                        sql = "COPY {table} FROM STDIN DELIMITER '{delimiter}' CSV HEADER;".format(** {
                            "table": table,
                            "delimiter": delimiter
                        })
                        cmd = "cat '{file}' | PGPASSWORD='{password}' psql -U {user} -d {dbname} -c \"{sql}\"".format(** {
                            "file": file_path,
                            "sql": sql,
                            "password": env["sparc2_db_password"],
                            "user": env["sparc2_db_user"],
                            "dbname":  env["sparc2_db_name"]
                        })
                        run(cmd)
        else:
            print "No files uploaded"
    else:
        abort("User requested abort.")


def _pipeline_export_shapefiles(**kwargs):

    local_path = request_input("Local File Path", kwargs.get("local_path", None), True)
    drop = request_input("Remote Drop Folder", kwargs.get("drop", None), True)

    tables = request_input("Database Tables (semicolon-separated)", kwargs.get("tables", None), True)
    sep = request_input("Table Separator (comma, semicolon, colon)", kwargs.get("sep", None), True, options=DB_TABLE_SEPARATORS)
    op = request_input("Operation", kwargs.get("op", None), True, options=DB_OPERATIONS)

    if request_continue():
        local("[ -d {d} ] || mkdir -p {d}".format(d=local_path))
        sudo("[ -d {d} ] || mkdir -p {d}".format(d=drop))
        sudo("chown {u}:{u} -R {d}".format(d=drop, u=env["user"]))
        if tables:
            with cd(drop):
                connstr = env["sparc2_connstr"]
                remote_files = []
                for table in tables.split(sep):
                    shapefile = "{table}.shp".format(table=table.replace(".", "_"))
                    shapefile_path = os.path.join(drop, shapefile)
                    shapefile_all = "{table}.*".format(table=table.replace(".", "_"))
                    flags = []
                    if op == "append":
                        flags.append("-append")
                    elif op == "replace":
                        flags.append("-overwrite")
                    cmd = 'ogr2ogr {flags} -f "ESRI Shapefile" {shapefile} PG:"{connstr}" {table}'.format(** {
                        "connstr": connstr,
                        "table": table,
                        "shapefile": shapefile_path,
                        "flags": " ".join(flags)
                    })
                    run(cmd)
                    remote_files.append(shapefile_all)

            if remote_files:
                for remote_file in remote_files:
                    remote_path = os.path.join(drop, shapefile_all)
                    get(remote_path, local_path)
    else:
        abort("User requested abort.")


def _pipeline_export_tables(**kwargs):

    local_path = request_input("Local File Path", kwargs.get("local_path", None), True)
    drop = request_input("Remote Drop Folder", kwargs.get("drop", None), True)

    tables = request_input("Database Tables (semicolon-separated)", kwargs.get("tables", None), True)
    sep = request_input("Table Separator (comma, semicolon, colon)", kwargs.get("sep", None), True, options=DB_TABLE_SEPARATORS)
    op = request_input("Operation", kwargs.get("op", None), True, options=DB_OPERATIONS)

    if request_continue():
        local("[ -d {d} ] || mkdir -p {d}".format(d=local_path))
        sudo("[ -d {d} ] || mkdir -p {d}".format(d=drop))
        sudo("chown {u}:{u} -R {d}".format(d=drop, u=env["user"]))
        if tables:
            with cd(drop):
                remote_files = []
                for table in tables.split(sep):
                    csv = "{table}.csv".format(table=table.replace(".", "_"))
                    csv_path = os.path.join(drop, csv)
                    sql = "COPY {table} TO STDOUT DELIMITER ',' CSV HEADER;".format(** {
                        "table": table
                    })
                    cmd = "echo \"{sql}\" | PGPASSWORD='{password}' psql -U {user} -d {dbname} {op} {path}".format(** {
                        "sql": sql,
                        "password": env["sparc2_db_password"],
                        "user": env["sparc2_db_user"],
                        "dbname":  env["sparc2_db_name"],
                        "op": (">" if op == "replace" else ">>"),
                        "path": csv_path
                    })
                    run(cmd)
                    remote_files.append(csv)
            if remote_files:
                for remote_file in remote_files:
                    remote_path = os.path.join(drop, remote_file)
                    get(remote_path, local_path)
    else:
        abort("User requested abort.")


def _pipeline_exec_sql(**kwargs):

    sql = kwargs.get("cmd", None)
    local_path = kwargs.get("local_path", None)
    drop = kwargs.get("drop", None)
    while (sql is None) == (local_path is None and drop is None):
        print "Please specify: (1) SQL command OR (2) a path to a local SQL file and a drop folder."
        sql = request_input("SQL Command", sql, False)
        local_path = request_input("Local File Path", local_path, False)
        drop = request_input("Remote Drop Folder", drop, False)

    if request_continue():
        if sql:
            cmd = "echo '{sql}' | PGPASSWORD='{password}' psql -U {user} -d {dbname}".format(** {
                "sql": sql.replace("'", "\\'"),
                "password": env["sparc2_db_password"],
                "user": env["sparc2_db_user"],
                "dbname":  env["sparc2_db_name"]
            })
            sudo(cmd)
        elif local_path:
            sudo("[ -d {d} ] || mkdir -p {d}".format(d=drop))
            remote_files = put(local_path, drop, mode='0444', use_sudo=True)
            if remote_files:
                with cd(drop):
                    for remote_file in remote_files:
                        sqlfile = None
                        if remote_file.endswith(".sql"):
                            sqlfile = remote_file
                        elif remote_file.endswith(".zip"):
                            sudo("unzip {f}".format(f=remote_file))
                            sqlfile = remote_file[0:-4] + ".sql"

                        if remote_file.endswith(".sql"):
                            cmd = "cat {f} | PGPASSWORD='{password}' psql -U {user} -d {dbname}".format(** {
                                "password": env["sparc2_db_password"],
                                "f": sqlfile,
                                "user": env["sparc2_db_user"],
                                "dbname":  env["sparc2_db_name"]
                            })
                            sudo(cmd)


def _pipeline_sql_schemas(**kwargs):

    schemas = request_input("Database Schemas (list separated by delimiter)", kwargs.get("schemas", None), True)
    sep = request_input("Schema Separator (comma, semicolon, colon)", kwargs.get("sep", None), True, options=DB_TABLE_SEPARATORS)

    if request_continue():
        for schema in schemas.split(sep):
            sql = "CREATE SCHEMA IF NOT EXISTS {schema};".format(schema=schema)
            cmd = "echo '{sql}' | PGPASSWORD='{password}' psql -U {user} -d {dbname}".format(** {
                "sql": sql.replace("'", "\\'"),
                "password": env["sparc2_db_password"],
                "user": env["sparc2_db_user"],
                "dbname":  env["sparc2_db_name"]
            })
            sudo(cmd)


def _pipeline_sql_clear(**kwargs):

    tables = request_input("Database Tables (semicolon-separated)", kwargs.get("tables", None), True)
    sep = request_input("Table Separator (comma, semicolon, colon)", kwargs.get("sep", None), True, options=DB_TABLE_SEPARATORS)

    if request_continue():
        for table in tables.split(sep):
            try:
                sql = "DELETE FROM {table};".format(table=table)
                cmd = "PGPASSWORD='{password}' psql -U {user} -d {dbname} -c \"{sql}\"".format(** {
                    "sql": sql,
                    "password": env["sparc2_db_password"],
                    "user": env["sparc2_db_user"],
                    "dbname":  env["sparc2_db_name"]
                })
                run(cmd)
            except:
                print "Tried to delete from non-existant table "+table+"."


def _pipeline_exec_python(**kwargs):

    local_path = request_input("Local File Path", kwargs.get("local_path", None), False)
    drop = request_input("Remote Drop Folder", kwargs.get("drop", None), False)
    chdir = request_input("chdir", kwargs.get("chdir", None), False)

    if request_continue():
        sudo("[ -d {d} ] || mkdir -p {d}".format(d=drop))
        remote_files = put(local_path, drop, mode='0444', use_sudo=True)
        if remote_files:
            for remote_file in remote_files:
                pyfile = None
                with cd(drop):
                    if remote_file.endswith(".py"):
                        pyfile = remote_file
                    elif remote_file.endswith(".zip"):
                        sudo("unzip {f}".format(f=remote_file))
                        pyfile = remote_file[0:-4] + ".py"
                if pyfile:
                    pycmd = "DJANGO_SETTINGS_MODULE=sparc2.settings"
                    pycmd += " "+env["sparc2_venv"]+"/bin/python"
                    pycmd += " "+os.path.join(drop, pyfile)
                    print pycmd
                    with cd(chdir):
                        sudo(pycmd, user=env["sparc2_user"])


def _pipeline_copy(**kwargs):

    src = request_input("Source File Path", kwargs.get("src", None), False)
    dest = request_input("Remote Destination Folder", kwargs.get("dest", None), False)

    if request_continue():
        sudo("[ -d {d} ] || mkdir -p {d}".format(d=dest))
        put(src, dest, mode='0444', use_sudo=True)

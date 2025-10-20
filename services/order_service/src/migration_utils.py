import subprocess

def run_flyway_migration():
    try:
        cmd = ["/usr/local/bin/flyway", "-configFiles=/app/flyway.conf", "migrate"]
        print("Flyway Migration Runing")
        result=subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("Migrations Output:\n", result.stdout)
    except subprocess.CalledProcessError as e:
        print("Flyway Migration Failed")
        print("STDOUT", e.stdout)
        print("STDOUT", e.stderr)
        raise
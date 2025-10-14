import mysql.connector
import matplotlib.pyplot as plt
plt.style.use('dark_background')

def database_request():
    conn = mysql.connector.connect(
        host="localhost",
        user="",
        password="",
        database="speedtesting"
    )
    cursor = conn.cursor()
    sql = "SELECT * FROM testings"
    cursor.execute(sql)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results


if __name__ == "__main__":
    result = database_request()
    times = []
    speeds = []
    for row in result:
        date = row[1]
        time = row[2]
        speed = float(row[3])
        times.append(f"{date} \n {time}h")
        speeds.append(speed)
    plt.figure(figsize=(10, 5))
    plt.plot(times, speeds, marker='.', linestyle='solid', markersize=0, color='silver')
    plt.title("Internet Speed Test")
    plt.xlabel("Time")
    plt.ylabel("Speed (Mbps)")
    plt.grid(True)
    plt.xticks([0, len(times) - 1], [times[0], times[-1]])
    plt.tight_layout()
    plt.show()

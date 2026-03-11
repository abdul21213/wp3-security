def get_vakken(conn, leerling_id):
    query = """
    SELECT DISTINCT v.vak_id, v.naam
    FROM dataset d
    JOIN vak v ON v.vak_id = d.vak_id
    WHERE d.leerling_id = ?
    ORDER BY v.naam
    """
    return conn.execute(query, (leerling_id,)).fetchall()


def get_leerdoelen(conn, leerling_id, vak_id):
    query = """
    SELECT l.leerdoel_id,
           l.titel,
           AVG((sc.kennen + sc.kunnen) / 2.0) AS gemiddelde
    FROM leerdoel l
    JOIN snapshot sn ON sn.leerdoel_id = l.leerdoel_id
    JOIN dataset d ON sn.dataset_id = d.dataset_id
    JOIN score sc ON sc.snapshot_id = sn.snapshot_id
    WHERE d.leerling_id = ?
      AND d.vak_id = ?
    GROUP BY l.leerdoel_id
    """
    return conn.execute(query, (leerling_id, vak_id)).fetchall()

def get_student_progress(conn, leerling_id, vak_id):
    query = """
        SELECT sn.datum AS date,
               AVG((sc.kennen + sc.kunnen) / 2.0) * 100 AS score
        FROM snapshot sn
        JOIN leerdoel l ON sn.leerdoel_id = l.leerdoel_id
        JOIN dataset d ON sn.dataset_id = d.dataset_id
        JOIN score sc ON sc.snapshot_id = sn.snapshot_id
        WHERE d.leerling_id = ?
          AND d.vak_id = ?
        GROUP BY sn.datum
        ORDER BY sn.datum
    """
    return conn.execute(query, (leerling_id, vak_id)).fetchall()
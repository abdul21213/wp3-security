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

def get_kernwoorden(conn, leerling_id, vak_id):
    query = """
    SELECT 
        l.titel AS leerdoel,
        k.woord AS kernwoord,
        AVG((sc.kennen + sc.kunnen) / 2.0) AS gemiddelde
    FROM leerdoel l
    JOIN snapshot sn ON sn.leerdoel_id = l.leerdoel_id
    JOIN dataset d ON sn.dataset_id = d.dataset_id
    JOIN score sc ON sc.snapshot_id = sn.snapshot_id
    JOIN leerdoel_kernwoord lk ON lk.leerdoel_id = l.leerdoel_id
    JOIN kernwoord k ON k.kernwoord_id = lk.kernwoord_id
    WHERE d.leerling_id = ?
      AND d.vak_id = ?
    GROUP BY l.leerdoel_id, k.kernwoord_id
    ORDER BY l.titel
    """
    return conn.execute(query, (leerling_id, vak_id)).fetchall()

def get_klassikale_vergelijking(conn, leerling_id, vak_id):
    query = """
    WITH mijn_klas AS (
        SELECT klas_id
        FROM leerling
        WHERE leerling_id = ?
    ),
    mijn_scores AS (
        SELECT l.leerdoel_id,
               l.titel,
               AVG((sc.kennen + sc.kunnen) / 2.0) AS mijn_gemiddelde
        FROM leerdoel l
        JOIN snapshot sn ON sn.leerdoel_id = l.leerdoel_id
        JOIN dataset d ON sn.dataset_id = d.dataset_id
        JOIN score sc ON sc.snapshot_id = sn.snapshot_id
        WHERE d.leerling_id = ?
          AND d.vak_id = ?
        GROUP BY l.leerdoel_id
    ),
    klas_scores AS (
        SELECT l.leerdoel_id,
               AVG((sc.kennen + sc.kunnen) / 2.0) AS klas_gemiddelde
        FROM leerdoel l
        JOIN snapshot sn ON sn.leerdoel_id = l.leerdoel_id
        JOIN dataset d ON sn.dataset_id = d.dataset_id
        JOIN score sc ON sc.snapshot_id = sn.snapshot_id
        JOIN leerling leer ON leer.leerling_id = d.leerling_id
        JOIN mijn_klas mk ON mk.klas_id = leer.klas_id
        WHERE d.vak_id = ?
        GROUP BY l.leerdoel_id
    )
    SELECT m.leerdoel_id,
           m.titel,
           m.mijn_gemiddelde,
           k.klas_gemiddelde
    FROM mijn_scores m
    LEFT JOIN klas_scores k ON k.leerdoel_id = m.leerdoel_id
    ORDER BY m.titel
    """
    return conn.execute(query, (leerling_id, leerling_id, vak_id, vak_id)).fetchall()

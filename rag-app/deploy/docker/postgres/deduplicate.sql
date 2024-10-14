DELETE FROM papers
WHERE
    id in (
        SELECT
            id
        FROM
            (
                SELECT
                    id,
                    title,
                    row_number() OVER (
                        PARTITION BY
                            title,
                            embedding
                        ORDER BY
                            id
                    )
                FROM
                    papers
            )
        WHERE
            row_number >= 2
    );
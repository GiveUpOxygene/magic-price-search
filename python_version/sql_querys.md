## traduction de la carte
```sql
SELECT f.name, c.name
FROM foreign_data f
JOIN cards c ON c.uuid=f.uuid
WHERE f.language='French'
GROUP BY f.uuid
```

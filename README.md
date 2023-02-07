# flask-rest-lsh
df train with flask and lsh

# Run the flask app
```
$ flask run
```

# Targets the endpoints
You target:
- /company to create companies in db or retrieve them with GET and POST requests
- /score/ID to score a specific company by ID


# The dataset
The dataset has name, revenue, id and accepted columns
```
                name  accepted  revenue  id
0  my_test_company_1      True      100   1
1  my_test_company_2      True      200   2
2  my_test_company_3      True      300   3
3  my_test_company_4      True      400   4
4  my_test_company_5     False       80   5
5  my_test_company_6     False       90   6
6  my_test_company_7     False       95   7
```

# Example POST
Creation of a company POSTing to /company
```
{
	"name": "my_test_company_7",
	"revenue": "95",
	"accepted": "false"
}
```

# Example GET
Score sending a GET request with ID to score
```
/score/2
```

# Result interpretation
A majority vote is used to determine the verdict
```
+--------+-------+---+--------+-----+--------------------+--------------------+
|accepted|revenue| id|features|label|     scaled_features|              hashes|
+--------+-------+---+--------+-----+--------------------+--------------------+
|    true|    100|  1| [100.0]|  1.0|[0.7950482616041498]|[[0.0], [-1.0], [...|
|    true|    200|  2| [200.0]|  1.0|[1.5900965232082995]|[[0.0], [-1.0], [...|
|    true|    300|  3| [300.0]|  1.0| [2.385144784812449]|[[1.0], [-2.0], [...|
|    true|    400|  4| [400.0]|  1.0| [3.180193046416599]|[[1.0], [-2.0], [...|
|   false|     80|  5|  [80.0]|  0.0|[0.6360386092833198]|[[0.0], [-1.0], [...|
|   false|     90|  6|  [90.0]|  0.0|[0.7155434354437348]|[[0.0], [-1.0], [...|
|   false|     95|  7|  [95.0]|  0.0|[0.7552958485239423]|[[0.0], [-1.0], [...|
+--------+-------+---+--------+-----+--------------------+--------------------+

+--------------------+--------------------+------------------+
|     scaled_features|              hashes|           distCol|
+--------------------+--------------------+------------------+
|[1.5900965232082995]|[[0.0], [-1.0], [...|               0.0|
|[0.7950482616041498]|[[0.0], [-1.0], [...|0.7950482616041498|
|[0.7552958485239423]|[[0.0], [-1.0], [...|0.8348006746843573|
|[0.7155434354437348]|[[0.0], [-1.0], [...|0.8745530877645648|
|[0.6360386092833198]|[[0.0], [-1.0], [...|0.9540579139249797|
+--------------------+--------------------+------------------+

+--------+
|accepted|
+--------+
|    true|
|   false|
|   false|
|   false|
+--------+

+--------+-----+
|accepted|count|
+--------+-----+
|   false|    3|
|    true|    1|
+--------+-----+

```

If in the neighbours we have more accepted than refused the company is scored as accepted.

The app will respond to the /score endpoint with a human readable answer such as:
```
{
	"message": "LSH credit acceptance: False."
}
```
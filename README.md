# flask-rest-lsh
df train with flask and lsh

# dataset
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

# create company POSTing to /company
```
{
	"name": "my_test_company_7",
	"revenue": "95",
	"accepted": "false"
}
```

# score sending a GET request with ID to score
```
/score/2
```
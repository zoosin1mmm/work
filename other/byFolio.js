Recursion 題目~
#1
n  f(n)
1  "1"
2  "212"
3  "32123"
4  "4321234"
5  "543212345"
function (n){
 if (n==1)  return 1 
 return n+""+function(n--)+""+n	
}


#2
n            max(n)
[1]          1
[3, 1]       3
[4, 3, 1]    4
function max(n) {
	i=n.lenght()
	return function array_max(n,i){
		if(i==1) return n[1]
		x=array_max(n,i-1)
		return x<n[i]?n[i]:x	
	}
}



#3
binarySearch(needle, ascToDescList), 給一個由小排到大的數字陣列，求裡面任一數字的index。
function binarySearch(needle,ascToDescList,i){
	if(needle==i) return ascToDescList[i]
	if(i==1) return 'not existing index or index over the array'
	return binarySearch(needle,ascToDescList,i-1)
}
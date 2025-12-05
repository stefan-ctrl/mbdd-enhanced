root = Node(1) 
root.left = Node(2) 
root.right = Node(3) 
root.left.left = Node(4) 
root.left.right = Node(5) 
root1 = Node(1);  
root1.left = Node(2);  
root1.right = Node(3);  
root1.left.left = Node(4);  
root1.right.left = Node(5);  
root1.right.right = Node(6);  
root1.right.right.right= Node(7);  
root1.right.right.right.right = Node(8)
root2 = Node(1) 
root2.left = Node(2) 
root2.right = Node(3) 
root2.left.left = Node(4) 
root2.left.right = Node(5)
root2.left.left.left = Node(6)
root2.left.left.right = Node(7)
assert (max_height(root)) == 3
assert (max_height(root1)) == 5 
assert (max_height(root2)) == 4

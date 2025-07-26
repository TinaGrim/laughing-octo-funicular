# Read the original file
with open("Driver1.py", "r") as source:
    content = source.read()

# Create 10 copies with different names
for i in range(2, 11):
    with open(f"Driver{i}.py", "w") as target:
        target.write(content)
    print(f"Driver{i}.py")
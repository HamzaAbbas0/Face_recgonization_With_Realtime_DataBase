import cv2

input_image_path = 'Images/452534.png'
output_image_path = '462534.png'
target_size = (216, 216)

# Read the input image
image = cv2.imread(input_image_path)

# Resize the image
resized_image = cv2.resize(image, target_size)

# Save the resized image in PNG format
cv2.imwrite(output_image_path, resized_image)

print(f"Image saved as {output_image_path}")

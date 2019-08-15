# images will be augmented
images_paths = []
# background images
backgrounds_paths = []

for root, dirs, files in os.walk('test/extracted_images/'):
    for file in tqdm(files):
        images_paths.append(os.path.join(root, file))
print('EXTRACTED IMAGES DONE')
        
for root, dirs, files in tqdm(os.walk('dtd/images/')):
    for file in files:
        backgrounds_paths.append(os.path.join(root, file))
        os.system('cls' if os.name == 'nt' else 'clear')
print('BACKGROUNDS DONE')

print(f'There will be {len(images_paths) * len(backgrounds_paths) * 8 } products in the folder..')
input('Please enter to continue..')

for counter, (img, back_img) in enumerate(product(images_paths, backgrounds_paths)):
    back_img = cv2.imread(back_img, 1)
    back_img = cv2.resize(back_img, (900, 900))
    
    back_img = random_rotate(back_img)
    back_img = np.array(back_img)
    
    img = cv2.imread(img, 1)
    img = cv2.resize(img, (300, 450))
    
    for i in range(0, 360, 45):
        resize_per = randint(50,100)/100
        
        background = back_img.copy()
        image = img.copy()
        image = cv2.resize(image, (0,0), fx=resize_per, fy=resize_per)
        image = imutils.rotate_bound(image, i)

        rows,cols,channels = img2.shape
        x_offset = int((background.shape[0]-image.shape[0])/2)
        y_offset = int((background.shape[1]-image.shape[1])/2)
		
		# Random coordinates to place the image
        rand_x = int(uniform(-x_offset, x_offset))
        rand_y = int(uniform(-y_offset, y_offset))
		
		# Black border needs to be removed after rotated the image
        roi = background[x_offset-rand_x:x_offset-rand_x+image.shape[0], 
                           y_offset-rand_y:y_offset-rand_y+image.shape[1]]
        imagegray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(imagegray, 10, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)
        background_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)
        image_fg = cv2.bitwise_and(image,image,mask = mask)
        dst = cv2.add(background_bg,image_fg)
        background[x_offset-rand_x:x_offset-rand_x+image.shape[0], 
                   y_offset-rand_y:y_offset-rand_y+image.shape[1]] = dst

        cv2.imwrite(f'test/{counter}_{i}.jpg', background)

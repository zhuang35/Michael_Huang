/* FILE: A2_bmp_helpers.c is where you will code your answers for Assignment 2.
 * 
 * Each of the functions below can be considered a start for you. 
 *
 * You should leave all of the code as is, except for what's surrounded
 * in comments like "REPLACE EVERTHING FROM HERE... TO HERE.
 *
 * The assignment document and the header A2_bmp_headers.h should help
 * to find out how to complete and test the functions. Good luck!
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <assert.h>

int bmp_open( char* bmp_filename,        unsigned int *width, 
              unsigned int *height,      unsigned int *bits_per_pixel, 
              unsigned int *padding,     unsigned int *data_size, 
              unsigned int *data_offset, unsigned char** img_data ){

              
  // YOUR CODE FOR Q1 SHOULD REPLACE EVERYTHING FROM HERE


	FILE *bmpFile = fopen( bmp_filename, "rb" );
	
	// checking validity of file	
	if(bmpFile == NULL){
		return -1;
	}

	// checking validity of file header
	char b, m;
	fread (&b, 1, 1, bmpFile);
	fread (&m, 1, 1, bmpFile);

	if((b != 'B') || (m != 'M')){
			return -1;
	}
	
	// obtains data size
	fread(data_size, 1, sizeof(unsigned int), bmpFile);
	
	// obtains width, height, bpp from standard header
	fseek(bmpFile, 0x12, SEEK_SET);
	fread(width, 4, 1, bmpFile);
	fseek(bmpFile, 0x16, SEEK_SET);
	fread(height, 4, 1, bmpFile);
	fseek(bmpFile, 0x1C, SEEK_SET);
	fread(bits_per_pixel, 4, 1, bmpFile);

	// calculates padding
	int temp = ((*width * 3) % 4);
	if(temp == 0){
		*padding = 0;
	} else{
		*padding = 4 - temp;
	}
	
	// obtains data offset from standard header
	fseek(bmpFile, 0xA, SEEK_SET);
	fread(data_offset, 4, 1, bmpFile);

	fseek(bmpFile, 0, SEEK_SET);

	// stores img_data in heap memory using malloc
	*img_data = (unsigned char*)malloc(*data_size);
	fread( *img_data, *data_size, 1, bmpFile);




	fclose(bmpFile);
	
	// TO HERE!




  
  return 0;  
}

// We've implemented bmp_close for you. No need to modify this function
void bmp_close( unsigned char **img_data ){

  if( *img_data != NULL ){
    free( *img_data );
    *img_data = NULL;
  }
}

int bmp_mask( char* input_bmp_filename, char* output_bmp_filename, 
              unsigned int x_min, unsigned int y_min, unsigned int x_max, unsigned int y_max,
              unsigned char red, unsigned char green, unsigned char blue )
{
  unsigned int img_width;
  unsigned int img_height;
  unsigned int bits_per_pixel;
  unsigned int data_size;
  unsigned int padding;
  unsigned int data_offset;
  unsigned char* img_data    = NULL;
  
  int open_return_code = bmp_open( input_bmp_filename, &img_width, &img_height, &bits_per_pixel, &padding, &data_size, &data_offset, &img_data ); 
  
  if( open_return_code ){ printf( "bmp_open failed. Returning from bmp_mask without attempting changes.\n" ); return -1; }
 
  // YOUR CODE FOR Q2 SHOULD REPLACE EVERYTHING FROM HERE
  
  
  FILE *fNew = fopen( output_bmp_filename, "wb" );
  
  char newbmp[data_size];
  
  memcpy( newbmp, img_data, data_size );
  
  // byteCounter is the index for the byte address
  int byteCounter = data_offset;

	// loops vertically through image
  for(int i = 0; i < img_height; i++){
		// loops horizontally through image
  	for(int j = 0; j < img_width; j++){
  		if((j >= x_min) && (j <= x_max) && (i >= y_min) && (i <= y_max)){
  			newbmp[byteCounter] = red;
  			newbmp[byteCounter + 1] = green;
  			newbmp[byteCounter + 2] = blue;
  		}
  		// increments counter by a pixel (3 bytes)
  		byteCounter = byteCounter + 3;
  	}
	// increments at the end of a row by the padding
	byteCounter = byteCounter + padding;
  }
  
	// writes to new file
  fwrite(newbmp, 1, data_size, fNew);
  
  
  
  // TO HERE!
  
  bmp_close( &img_data );
  
  return 0;
}         

int bmp_collage( char* bmp_input1, char* bmp_input2, char* bmp_result, int x_offset, int y_offset ){

  unsigned int img_width1;
  unsigned int img_height1;
  unsigned int bits_per_pixel1;
  unsigned int data_size1;
  unsigned int padding1;
  unsigned int data_offset1;
  unsigned char* img_data1    = NULL;
  
  int open_return_code = bmp_open( bmp_input1, &img_width1, &img_height1, &bits_per_pixel1, &padding1, &data_size1, &data_offset1, &img_data1 ); 
  
  if( open_return_code ){ printf( "bmp_open failed for %s. Returning from bmp_collage without attempting changes.\n", bmp_input1 ); return -1; }
  
  unsigned int img_width2;
  unsigned int img_height2;
  unsigned int bits_per_pixel2;
  unsigned int data_size2;
  unsigned int padding2;
  unsigned int data_offset2;
  unsigned char* img_data2    = NULL;
  
  open_return_code = bmp_open( bmp_input2, &img_width2, &img_height2, &bits_per_pixel2, &padding2, &data_size2, &data_offset2, &img_data2 ); 
  
  if( open_return_code ){ printf( "bmp_open failed for %s. Returning from bmp_collage without attempting changes.\n", bmp_input2 ); return -1; }
  
  // YOUR CODE FOR Q3 SHOULD REPLACE EVERYTHING FROM HERE

	// sorts and finds the larger/smaller widths
	int largerH, smallerH, largerW, smallerW;
	
	if(img_height1 > img_height2){
		largerH = img_height1;
		smallerH = img_height2;
	} else{
		largerH = img_height2;
		smallerH = img_height1;
	}
	
	if(img_width1 > img_width2){
		largerW = img_width1;
		smallerW = img_width2;
	} else{
		largerW = img_width2;
		smallerW = img_width1;
	}
	
		
	int newHeight = largerH;
	int newWidth = largerW;
	
	// calculates the width and height of new image based on offset and larger image
	int tempX, tempY;
	
	
	// finds the new width based on offsets, checking if the two images overlap
	if(x_offset >= 0){
		if((img_width2 + x_offset) > img_width1){
			newWidth = img_width2 + x_offset;	
		} else {
			newWidth = img_width1;
		}
	} else{
		if((img_width2 - x_offset) > img_width1){
			newWidth = largerW - x_offset;
		} else{
			newWidth = img_width1 - x_offset;
		}
	}

	if(y_offset >= 0){
		if((img_height2 + y_offset) > img_height1){
			newHeight = img_height2 + y_offset;	
		} else{
			newHeight = img_height1;
		}
	} else{
		if((img_height2 - y_offset) > img_height1){
			newHeight = largerH - y_offset;
		} else{
			newHeight = img_height1 - y_offset;
		}
	}
	

	
	// calculates the padding for the new image
	int newPadding = ((newWidth * 3) % 4);
	if(newPadding != 0){
		newPadding = 4 - newPadding;
	}




	// finds the size of the new image
	int newSpace = (newWidth * bits_per_pixel1 / 8 + newPadding) * newHeight;
	newSpace = newSpace + data_offset1;
	
	// initializes a char array to store the data for the collaged image
	char newbmp[newSpace];
	for(int i = 0; i < newSpace; i++){
		newbmp[i] = 255;
	}
	
	// copies in header information from image1
	memcpy(newbmp, img_data1, data_offset1);

	
	int byteCounter = 0;
	int initialX = 0;
	int initialY = 0;
	
	// calculates the initial X,Y position for the bottom left relative to image1
	if(x_offset < 0){
		initialX = abs(x_offset);
	}
	if(y_offset < 0){
		initialY = abs(y_offset);
	}
	

	
	int rowCounter = 0;
	// byteCounter1 indexes image1 relative to itself
	int byteCounter1 = data_offset1;
	for(int i = 0; i < img_height1; i++){
		// adjusts the byteCounter relative to the row it is at
		byteCounter = data_offset1 + (3 * initialX) + ((newPadding + 3 * newWidth) * (initialY + i));
		for(int j = 0; j < img_width1; j++){
			// copies the pixel from img_data1
			newbmp[byteCounter] = img_data1[byteCounter1];
			newbmp[byteCounter + 1] = img_data1[byteCounter1 + 1];
			newbmp[byteCounter + 2] = img_data1[byteCounter1 + 2];
			
			// increment byteCounters relative to the bmp it is pointing at
			byteCounter = byteCounter + 3;
			byteCounter1 = byteCounter1 + 3;
		}
		// increments by padding
		byteCounter1 = byteCounter1 + padding1;
	}
	





	// calculates the initial X,Y position relative to image2
	initialX = 0;
	initialY = 0;
	if(x_offset > 0){
		initialX = x_offset;
	}
	if(y_offset > 0){
		initialY = y_offset;
	}
	
	
	// same logic as above but with image2 and image2 parameters
	int byteCounter2 = data_offset2;
	for(int i = 0; i < img_height2; i++){
		byteCounter = data_offset1 + (3 * initialX) + ((newPadding + 3 * newWidth) * (initialY + i));
		for(int j = 0; j < img_width2; j++){
			newbmp[byteCounter] = img_data2[byteCounter2];
			newbmp[byteCounter + 1] = img_data2[byteCounter2 + 1];
			newbmp[byteCounter + 2] = img_data2[byteCounter2 + 2];
			
			byteCounter = byteCounter + 3;
			byteCounter2 = byteCounter2 + 3;
		}
		byteCounter2 = byteCounter2 + padding2;
	}
	

	
	// writes to new file
	FILE* newFile = fopen( bmp_result, "wb+" );
	// copies in entire newbmp char array
	fwrite(newbmp, 1, newSpace, newFile);
	
	// overwrites parts of header with new width, height, and space
	fseek(newFile, 0x12, SEEK_SET);
	fwrite(&newWidth, 4, 1, newFile);
	fseek(newFile, 0x16, SEEK_SET);
	fwrite(&newHeight, 4, 1, newFile);
	fseek(newFile, 0x2, SEEK_SET);
	fwrite(&newSpace, 4, 1, newFile);
	
	fclose(newFile);
	


  // TO HERE!
      
  bmp_close( &img_data1 );
  bmp_close( &img_data2 );
  
  return 0;
}                  

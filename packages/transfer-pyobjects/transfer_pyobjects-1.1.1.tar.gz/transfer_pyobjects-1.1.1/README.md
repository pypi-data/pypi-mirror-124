hello, you may use this program

it was originally intended for transfer of AIs between computers,
but this functionaly allows for variables to be stored in disk, and not ram
this can be built on to allow the transfer of veriables in say a hosted
python notebook. this means you can build and save a value easily. just
remember to import all required modules for the pyobject, otherwise
it will not work.

Functions:
  read_obj(filename)
    takes a filename as input and returns a pyobject contained in the file
    
   write_obj(content, filename)
     takes 2 args, the filename, and the content. the content is the variable to be written, the filename
     is the location of the file to write.

# The dimension class is merely a class to hold the
# width and height of an area. Not much more than a tuple,
# but referring to values by .width and .height makes the
# code clearer than refering to values by [0] and [1].
#
# TO DO: Initialize width and height attributes for
#        Dimension objects. They should be set to the values
#        received as parameters to the constructor
# HINT:  To add an attribute, add its identifier to self and
#        assign it a value. For example, adding an attribute
#        called foo with no value would look like: 
#        self.foo = None
class Dimension:
  def __init__( self, width, height ):
    self.width = 0
    self.height = 0

# TESTS! To run these, run: python dimension.py 
# All tests must pass for you to get full credit.
# DO NOT CHANGE ANYTHING BELOW THIS LINE!
if __name__ == '__main__':
  for test in (
    (0, 0), (1,1), (2,3), (3,2)
  ):
    temp = Dimension( test[0], test[1] )
    if ( temp.width == test[0] ):
      print ("OK")
    else:
      print( "temp=Dimension(%d,%d); expected temp.width to be %d, got %d"%(test[0],test[1],test[0],temp.width) )
    if ( temp.height == test[1] ):
      print ("OK")
    else:
      print( "temp=Dimension(%d,%d); expected temp.height to be %d, got %d"%(test[0],test[1],test[1],temp.height) )

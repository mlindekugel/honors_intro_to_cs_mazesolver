# The Point class represents a position on a grid. It uses
# screen coordinates, not Cartesian coordinates. This means
# that 0,0 is the top left corner of the grid, not the center.
# Like the Cartesian coordinate system, as x increases, the
# point moves right; unlike Cartesian coordinates, as y 
# increases, you move DOWN. There are no negative values in
# the screen coordinate system.
class Point:
  # Initialize the object with values for x and y
  def __init__( self, x, y ):
    self.x = x
    self.y = y
  
  # Determine if this point is with the rectangle. The 
  # rectangle is defined by a tuple containing the Point 
  # in the rectangle's top left corner and the Point in 
  # its bottom right corner. 
  def is_in_rect( self, rect ):
    topLeft = rect[0]
    bottomRight = rect[1]
    # If this point's x value is greater or equal to the
    # furthest left point's x and smaller or equal to the 
    # furthest right point's x and this point's y is 
    # greater than or equal to the topmost point's y and 
    # less than or equal to the lowest point's y,
    # then it is with the bounds of the rectangle.

    # TO DO: Implement this function
    # HINT:  This point's x and y coordinates are available
    #        on the "self" variable, which points to this 
    #        object's data; the x and y values of topLeft 
    #        and bottomRight are accessed through those
    #        variables (ie topLeft.x)
    return True
  
  # Translate a point from the wavefront grid to a point
  # in the image.
  def as_image( self, maze ):
    return Point( self.x * maze.path_width, 
                  self.y * maze.path_width )

  # Translate a point from the image grid to a point in
  # the wavefront grid.
  def as_wave( self, maze ):
    return Point( self.x // maze.path_width, 
                  self.y // maze.path_width )

  # Get the rectangle surrounding this point. The rectangle
  # is specified by a Dimension that says how wide and how
  # tall the rectangle should be. This point should be as
  # close to the center of the rectangle as possible.
  def get_rect_around( self, area ):
    left = area.width // -2 + area.width % 2;
    top = area.height // -2 + area.height % 2;
    right = left + area.width
    bottom = top + area.height
    return ( Point(left + self.x, top + self.y), 
             Point(right + self.x, bottom + self.y ) )
  
  def __str__( self ):
    return "Point(%d,%d)"%(self.x, self.y)

# TESTS! To run these, run: python point.py 
# All tests must pass for you to get full credit.
# DO NOT CHANGE ANYTHING BELOW THIS LINE!
if __name__ == '__main__':
  rect = ( Point(2,2), Point(6,4) )
  for test in ( 
    Point(1,1), Point(3,1), Point(7,1), # ABOVE 
    Point(1,3), Point(7,3), # SIDES 
    Point(0,5), Point(4,5), Point(8,5), # BELOW 
  ):
    value=test.is_in_rect( rect )
    if value == False :
      print( "OK" )
    else:
      print( "%s.is_in_rect(( %s,%s )) expected False, got %s"%(test,rect[0],rect[1],value) )
  for test in ( 
    Point(2,2), Point(4,2), Point(6,2), # On top border
    Point(2,3), Point(5,3), Point(6,3), # On sides or inside
    Point(2,4), Point(4,4), Point(6,4), # On bottom border
  ):
    value=test.is_in_rect( rect )
    if value == True :
      print( "OK" )
    else:
      print( "%s.is_in_rect(( %s,%s )) expected True, got %s"%(test,rect[0],rect[1],value) )

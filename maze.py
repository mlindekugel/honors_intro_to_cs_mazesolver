from PIL import Image, ImageDraw
from dimension import Dimension
from point import Point

# The Maze class does the bulk of the work. As a whole, it's
# reasonably complex. But notice that, through abstraction,
# each method performs just one task and is reasonably 
# comprehensible.
class Maze:
  # Load the image from disk if image is specified as a string,
  # otherwise return the image. Note that this is a static
  # method. It belongs to the Maze class, so won't conflict
  # if any code outside of Maze also were to have a load_image()
  # function, BUT it doesn't get a reference to an object's data
  # (self) as a parameter. 
  def load_image(image):
    if type(image) == str:
      temp = Image.open(image)
      return temp.convert("RGBA")
    else:
      return image
  
  # Construct a Maze object. All that is required is an image 
  # or filename for the mage. Optional arguments are: 
  # start Point, 
  # end Point, 
  # crop (list of 2 Points indicating top left corner and
  #       bottom right corner), 
  # path_width (an int indicating how wide the paths are.)
  # The crop is needed for many mazes because the margins around
  # the maze often is light, like the paths in the maze. You 
  # need to crop out the margin to prevent the algorithm from
  # getting to start to end by going around the maze itself.
  # Notice that in python, required arguments don't have any
  # default value; after all the required arguments, you can
  # specify optional arguments which, if not provided, will
  # get the value specified in the method header.  
  def __init__( self, image, start=Point(0,0), \
                end=None, crop=[ Point(0,0), None ], path_width=3 ):
    self.start, self.end = ( start, end )
    self.image = Maze.load_image(image)
    self.image_limits = ( \
      Point(0,0), \
      Point(self.image.width-1,self.image.height-1) )
    self.crop = crop
    self.path_width = path_width
    self.waves = None
    if end == None:
      self.end = Point(self.image.width-1, self.image.height-1)
    if crop[1] == None:
      crop[1] = Point(self.image.width-1, self.image.height-1)
    self.pointA, self.pointB = None, None
    # Calculate reasonable values to indicate a BLOCKED passage
    # and a passage that has not yet been populated. These
    # values depend on the overall size of the maze. 
    self.BLOCKED = self.image.width * self.image.height + 1
    self.UNPOPULATED = self.BLOCKED - 1

  def save( self, filename ):
    self.image.save( filename )

  # We can speed the algorithm and reduce memory usage by 
  # storing wave data in a smaller array than the image data.
  # Image data needs to distinguish each pixel, but each 
  # element in the wave merely reflects a square the size of
  # the width of the path.
  # To keep the code clear and consistent, these two methods
  # abstract those calculations.
  def wave_height( self ):
    return self.image.height // self.path_width
  
  def wave_width( self ):
    return self.image.width // self.path_width

  # THE FOLLOWING SECTION METHODS ARE ALL DEDICATED TO 
  # EXECUTING THE LOGIC FOR INITIALIZING THE WAVE. THIS 
  # COULD ALL BE DONE IN ONE METHOD, BUT HOPEFULLY YOU
  # SEE HOW PUTTING EACH "JOB" IN A SEPARATE METHOD MAKES
  # EACH ALGORITHM, AS WELL AS THE OVERALL ALGORITHM, MORE
  # READABLE (AND TESTABLE!)

  # Initialize the wave array. This is a two-dimensional array.
  # The first dimension holds the columns, the second the rows.
  # This is different than the way we did it in VEX, but is
  # consistent with the way the Point class is laid out. 
  def initialize_wave( self ):
    width, height = self.wave_width(), self.wave_height()
    # Notice how you can use the * operator to quickly create
    # an array. In this case, we create an array of Nones
    # that is the size of the total width that we want.
    self.waves = [None] * width
    # Now, for each column we just created, create an array
    # of rows. Each row's value is assumed to be unpopulated.
    for col in range( width ):
      self.waves[col] = [self.UNPOPULATED] * height
    # Finally, mark all the areas that are blocked.
    self.mark_blocked_areas()

  # Simply check each element in the wave array to see if its
  # equivalent point in the image is blocked. 
  def mark_blocked_areas( self ):
    width, height = self.wave_width(), self.wave_height()
    for col in range( width ):
      for row in range( height ):
        if self.is_blocked( Point(col, row).as_image(self) ):
          self.waves[col][row] = self.BLOCKED

  # To determine if a Point in the image is blocked, first
  # check to see if it is outside the crop area (if it is, it's
  # blocked). Otherwise, look to see if anything in 
  # the area is blocked. The size of the area around this point # depends on the maze's path width.
  def is_blocked( self, point ):
    if not point.is_in_rect( self.crop ):
       return True
    area = Dimension(self.path_width,self.path_width)
    return self.area_is_blocked(point, area)

  # To determine if the area is blocked, look at each pixel.
  # If the average of the pixel's red, green, and blue values
  # (pixel[0], pixel[1], and pixel[2]) is less than 128, it's
  # dark and we can assume that it's blocked. One dark pixel
  # in the area is all it takes to block the entire area!
  def area_is_blocked( self, point, area ):
    topLeft, bottomRight = point.get_rect_around( area )
    for x in range( topLeft.x, bottomRight.x ):
      for y in range( topLeft.y, bottomRight.y ):
        check = Point(x, y)
        if check.is_in_rect( self.image_limits ):
          pixel = self.image.getpixel( (check.x, check.y) )
          avg = (pixel[0] + pixel[1] + pixel[2]) / 3
          if avg < 128:
            return True
    return False

  # THAT CONCLUDES METHODS FOR INITIALIZING THE WAVE
  # BELOW ARE METHODS FOR CALCULATING THE WAVES FROM 
  # END TO START.

  # The points list initialized at the beginning of 
  # calculate_waves is "just a list." But we are using it
  # in the form of a "queue." A queue operates like a line
  # at the grocery store check-out line. Each new person
  # is added to the end of the line in the order in which
  # they came, while people are checked out starting at the
  # beginning of the line. The code loops until everything
  # that appeared in the queue has been processed.
  def calculate_waves(self):
    # Initialize the queue; to start, there is just one point:
    # The end point of the maze.
    points = [self.end.as_wave(self)]
    # Set the current wave to 1.
    current_wave = 1
    # idx tracks where we are in the list (how many Points
    # have been processed so far.)
    idx = 0
    # Determine when to increase the wave. Once we've processed
    # all the points that are currently available, we'll 
    # increase the wave.
    increase_wave = len( points )
    # While wave not not processed all the points in the queue...
    while idx < len( points ):
      # Set the wave value for all points surrounding this one
      self.set_wave_around_point( points, idx, current_wave )
      # We've processed this point, so increment idx
      idx = idx + 1
      # If we've processed all points for the current wave, 
      # increment current_wave and determine when the next
      # time the wave must be incremented will be
      if idx == increase_wave:
        current_wave = current_wave + 1
        increase_wave = len(points)

  # Unlike in VEX, when we were limited to north, south,
  # east, and west, in a maze, we can move diagonally. Set
  # the surrounding points to the current wave.
  def set_wave_around_point( self, points, idx, wave ):
    cp = points[ idx ]
    for x in range( -1, 2 ):
      for y in range( -1, 2 ):
        pt = Point(cp.x + x, cp.y + y)
        self.set_wave_for_point(pt.as_image(self), wave, points)

  # Set the wave value for this point, but only if it's within
  # the cropped area AND it's not already populated. It could
  # be populated if it was found to be blocked during initial-
  # ization or if a previous wave already set it.
  def set_wave_for_point( self, point, wave, points ):
    if point.is_in_rect(self.crop):
      # Remember, this point is in the image. To mark the
      # appropriate location in the wave array, map it to
      # the wave coordinates.
      wp = point.as_wave(self)
      if self.waves[wp.x][wp.y] == self.UNPOPULATED:
        self.waves[wp.x][wp.y] = wave
        points.append(wp)

  # THAT CONCLUDES THE METHODS FOR CALCULATING THE WAVES!
  # THE FOLLOWING METHODS DRAW THE LINE ONCE THE WAVES HAVE
  # BEEN CALCULATED

  # The basic algorithm is, start at the start, go to the 
  # smallest surrounding wave value and draw a 
  # line from the previous point to the current point. 
  # Repeat until the point you go to is the end.
  def plot_course( self, color=(255,0,0) ):
    point = self.start.as_wave(self)
    # Initialize the point to go to as this point; if we
    # ever find the point we're going to is the same as the
    # point we're on, we know that no path through the maze
    # was found by the waves (probably the path_width was too
    # big, or maybe there really is no solution!)
    go = point
    last_point, this_point = None, None
    # Get a drawing context for the image; this makes it easier
    # to draw lines between two points (rather than doing the
    # math ourselves)
    draw = ImageDraw.Draw(self.image)
    # While we still are not at the end
    while self.still_plotting( point ):
      # Move the point we came from to the previous point,
      # and set the current point. 
      last_point = this_point
      this_point = point.as_image(self)
      # Draw a line between the two points
      self.connect( draw, last_point, this_point, color )
      # Find the next point by searching for the smallest
      # neighboring point
      go = self.smallest_neighbor( point )
      # If the smallest point is the one we're one, we're stuck.
      if go == point:
        print( "Unable to find path through maze." )
        return
      # Update the current point to the one we want to go to
      point = go
    # Connect the final processed point to the end point.
    self.connect( draw, this_point, self.end, color )
    # We don't need to draw on the maze anymore; delete the
    # drawing context.
    del draw

  # This is just a utility to make the previous algorithm
  # easier to read.
  def still_plotting( self, point ):
    return self.waves[point.x][point.y] > 1    

  # Assuming neither pointA or pointB is None, draw a line
  # between them.
  def connect(self, draw, pointA, pointB, color ):
    pass

  # Return the smallest neighbor around a point
  def smallest_neighbor( self, point ):
    go = point
    for row in range( -1, 2 ):
      for col in range( -1, 2 ):
        check = Point( point.x + col, point.y + row )
        if not check.is_in_rect( self.image_limits ):
          continue
        if self.waves[check.x][check.y] < self.waves[go.x][go.y]:
          go = check
    return go

  # OK, it took a lot of code to get here... but look how
  # simple the algorithm actually is when you remove
  # the details through abstraction and focus on the 
  # "big picture."
  def solve(self, color=(255,0,0) ):
    print( "Initializing wave... ")
    self.initialize_wave()
    print( "Calculating wave... ")
    self.calculate_waves()
    print( "Plotting course... ")
    self.plot_course(color)


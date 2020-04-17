from maze import Maze
from point import Point

start=Point(90,70)
end=Point(420,346)
crop=( Point(35,27), Point(490,376) )
maze = Maze("maze1.png", start=start, end=end, crop=crop,path_width=4)
maze.solve( color=(128, 0, 0))
maze.save('test1.png')

start=Point(55,55)
end=Point(545,545)
crop=( Point(9,9), Point(591,591) )
maze = Maze("maze2.jpg", start, end, crop, path_width=3)
maze.solve( color=(255, 128, 0))
maze.save('test2.png')

start=Point(10,572)
end=Point(1118,572)
crop=( Point(12,12), Point(1115,1130) )
maze = Maze("maze3.png", start, end, crop, path_width=8)
maze.solve( color=(128, 255, 0))
maze.save('test3.png')

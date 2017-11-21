from unittest import TestCase
from dem_sim.objects.cv import CV


class TestCV(TestCase):
    def test_set_neighbors(self):
        cvs = []

        for i in range(3):
            for j in range(3):
                for k in range(3):
                    cvs.append(CV([i, j, k]))

        for cv in cvs:
            cv.set_neighbors(cvs)

        for cv in cvs:
            print("CV = " + str(cv) + "\nNeighbors =")
            for neighbor in cv.neighbors:
                print(str(neighbor))

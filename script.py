import unittest
class TestPortExclusion(unittest.TestCase):

    def apply_port_exclusions(self, include_ports, exclude_ports):
        ports = []

        # if include_ports is empty we just return an empty list 
        if include_ports is []:
            return ports
    
        minified_ports = self.minify_array(include_ports)

        # if exclude_ports is empty then we can just return the minified array
        if exclude_ports is []:
            return minified_ports
        
        return self.remove_excluded_ports(minified_ports, exclude_ports)
    
    def minify_array(self, ports):
        minified_array = []

        # We sort ports here in place to make sure the list is now ordered
        ports.sort()
        minified_array[0] = ports.sort().pop(0)

        for pair in ports:
            if minified_array[-1][-1] >= pair[0] or minified_array[-1][-1] >= pair[0]-1:
                minified_array[-1][-1] = pair[-1]
            else:
                minified_array.append(pair)


        return minified_array

    def remove_excluded_ports(self, minified_array, excluded_ports):
        ports = []

        for exclude_pair in excluded_ports:
            for include_pair in minified_array:
                if exclude_pair[1] >= include_pair[0] and exclude_pair[0] <= include_pair[0]:
                    add = 1 if exclude_pair[1] - exclude_pair[0] == 0 else exclude_pair[1] - exclude_pair[0]
                    ports.append([include_pair[0]+add, include_pair[1]])
                elif exclude_pair[0] > include_pair[0] and exclude_pair[1] < include_pair[1]:
                    ports.append([include_pair[0],exclude_pair[0]-1])
                    ports.append([exclude_pair[1]+1, include_pair[1]])
                elif exclude_pair[0] > include_pair[0] and exclude_pair[1] <= include_pair[1]:
                    ports.append([include_pair[0],exclude_pair[0]-1])
    

        return ports
    
    def test_1(self):
        include_ports = [[80, 80], [22, 23], [8000, 9000]]
        exclude_ports = [[1024, 1024], [8080, 8080]]
        output = [[22, 23], [80, 80], [8000, 8079], [8081, 9000]]
        self.assertEqual(output, self.apply_port_exclusions(include_ports, exclude_ports))

    def test_2(self):
        include_ports = [[8000, 9000], [80, 80], [22, 23]]
        exclude_ports = [[1024, 1024], [8080, 8080]]
        output = [[22, 23], [80, 80], [8000, 8079], [8081, 9000]]
        self.assertEqual(output, self.apply_port_exclusions(include_ports, exclude_ports))

    def test_3(self):
        include_ports = [[1,1], [3, 65535], [2, 2]]
        exclude_ports = [[1000, 2000], [500, 2500]]
        output = [[1, 499], [2501, 65535]]
        self.assertEqual(output, self.apply_port_exclusions(include_ports, exclude_ports))

    def test_4(self):
        include_ports = [[1,65535]]
        exclude_ports = [[1000,2000], [500, 2500]]
        output = [[1, 499], [2501, 65535]] 
        self.assertEqual(output, self.apply_port_exclusions(include_ports, exclude_ports))

    def test_5(self):
        include_ports = []
        exclude_ports = [[1024, 1024], [8080, 8080]]
        output = []
        self.assertEqual(output, self.apply_port_exclusions(include_ports, exclude_ports))

    def test_6(self):
        include_ports = [[80, 80], [22, 23], [8000, 9000]]
        exclude_ports = []
        output = [[22, 23], [80, 80], [8000, 9000]]
        self.assertEqual(output, self.apply_port_exclusions(include_ports, exclude_ports))

if __name__ == '__main__':
    unittest.main()
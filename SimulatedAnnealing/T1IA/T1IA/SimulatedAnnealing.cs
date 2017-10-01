using System;
using System.Collections.Generic;
using System.IO;

namespace T1IA
{
    class SimulatedAnnealing
    {
        //Matrix to store the data
        int[,] dataMatrix;

        //Dimension of the matrix
        int dimension = 0;

        //Temperature
        float initTemp = 500;
        float temp;

        //Temperature cooldown multiplier
        float mult = 0.9983f;
        
        //Current solution
        List<int> current;

        //Best solution
        List<int> bestSolution;
        int distance;

        //Random
        Random rand = new Random();

        /// <summary>
        /// Reads the file at given path and structures it's data
        /// </summary>
        /// <param name="path">the file's path</param>
        /// <returns>true if successfull</returns>
        public bool ReadFile(string path)
        {
            //Reads all the lines in the file and stores them separately
            string[] lines = File.ReadAllLines(path);
            string[] stringSeparators = new string[] { " " };
            
            //Stores the data
            string dataText = "";
            string[] data;
            
            bool readData = false;
            bool lowerDiag = false;

            foreach (string line in lines)
            {
                if (line.Contains("DIMENSION:"))
                {
                    //Stores the matrix dimension
                    dimension = Int32.Parse(line.Split(stringSeparators, StringSplitOptions.None)[1]);
                }
                else if (line.Contains("EDGE_WEIGHT_FORMAT:"))
                {
                    if (line.Contains("LOWER_DIAG_ROW"))
                    {
                        lowerDiag = true;
                    }
                }
                else if (line.Contains("EDGE_WEIGHT_SECTION"))
                {
                    //Last line before data. Flag set to true
                    readData = true;
                }
                else if (readData && !line.Contains("EOF"))
                {
                    //Concatenates all the lines with data
                    dataText = String.Concat(dataText, line);
                }
            }

            //Separates the data in the array
            data = dataText.Split(stringSeparators, StringSplitOptions.RemoveEmptyEntries);

            dataMatrix = new int[dimension, dimension];
            int next = 0;

            //Stores the data based on the structure given in the file
            if (lowerDiag)
            {
                if (dimension != 0)
                {
                    for (int i = 0; i < dimension; i++)
                    {
                        for (int j = 0; j < i+1; j++)
                        {
                            dataMatrix[i, j] = Int32.Parse(data[next]);
                            dataMatrix[j, i] = Int32.Parse(data[next]);
                            next++;
                        }
                    }
                }
                else
                {
                    Console.WriteLine("Error: dimension 0\n");
                    return false;
                }
            }
            else
            {
                if (dimension != 0)
                {
                    for (int i = dimension - 1; i >= 0; i--)
                    {
                        for (int j = i; j >= 0; j--)
                        {
                            dataMatrix[i, j] = Int32.Parse(data[next]);
                            dataMatrix[j, i] = Int32.Parse(data[next]);
                            next++;
                        }
                    }
                }
                else
                {
                    Console.WriteLine("Error: dimension 0\n");
                    return false;
                }
            }

            return true;
        }

        /// <summary>
        /// Calculates the TSP solution
        /// </summary>
        /// <returns>the solution</returns>
        public void CalculateTSP()
        {
            //Next solution
            List<int> next;

            //Generates first solution
            current = GenerateSolution();

            int count = 0;
            int deltaE;
            
            //Iterates until max allowed
            while (count < dimension)
            {
                temp = initTemp;
                while(temp > 0.001)
                {
                    //Updates the temperature
                    CalculateTemp();

                    //Generates next solution
                    next = GenerateSolution();

                    //Calculates the value difference
                    deltaE = CalculateDistance(current) - CalculateDistance(next);

                    //Next solution is better than current (Downhill)
                    if (deltaE > 0)
                    {
                        current = next;
                    }
                    //Next solution is worse than current (Uphill)
                    else
                    {
                        //Calculates the probability to choose the solution
                        if (rand.NextDouble() <= Math.Exp(deltaE / temp))
                        {
                            current = next;
                        }
                    }
                }

                if(bestSolution == null || CalculateDistance(current) < CalculateDistance(bestSolution))
                {
                    bestSolution = current;
                }
                
                count++;
            }
            
            Console.WriteLine("Caminho: \n");
            foreach (int n in bestSolution)
            {
                Console.Write(n + " - ");
            }
            distance = CalculateDistance(bestSolution);
            Console.WriteLine("\nPeso: " + distance);
        }

        /// <summary>
        /// Calculates the solution distance
        /// </summary>
        /// <param name="solution">solution</param>
        /// <returns>solution distance</returns>
        int CalculateDistance(List<int> solution)
        {
            //Total distance
            int totalDistance = 0;

            //Increments total distance by each distance
            for(int i = 0; i < dimension; i++)
            {
                totalDistance += dataMatrix[solution[i], solution[(i + 1) % dimension]];
            }

            return totalDistance;
        }
        
        /// <summary>
        /// Generates a new solution based on the current solution
        /// </summary>
        /// <returns>new solution</returns>
        List<int> GenerateSolution()
        {
            List<int> newSolution = new List<int>(dimension);
            
            //If current is null, generates a random solution
            if(current == null)
            {
                for (int i = 0; i < dimension; i++)
                {
                    newSolution.Add(i);
                }

                int n = newSolution.Count;
                while (n > 1)
                {
                    n--;
                    int k = rand.Next(n + 1);
                    int value = newSolution[k];
                    newSolution[k] = newSolution[n];
                    newSolution[n] = value;
                }
            }
            else
            {
                //Perfoms a 2-opt   


                //Clones the current solution
                foreach (int n in current)
                {
                    newSolution.Add(n);
                }

                int i;
                int j;
                do
                {
                    i = rand.Next(dimension);
                    j = rand.Next(dimension);
                } while (i == j);

                int min, max;
                if(i < j)
                {
                    min = i;
                    max = j;
                }
                else
                {
                    min = j;
                    max = i;
                }

                int diff = max - min;
                List<int> route = new List<int>(diff+1);

                //Clones the route
                for (int k = min; k <= max; k++)
                {
                    route.Add(newSolution[k]);
                }

                //Reverses the route inside the solution
                for (int k = 0; k <= diff; k++)
                {
                    newSolution[k+min] = route[diff-k];
                }
            }

            return newSolution;

        }

        /// <summary>
        /// Calculates the new temperature
        /// </summary>
        void CalculateTemp()
        {
            temp *= mult;
        }

        public void getParameters(ref List<int> sol, ref float coolFactor, ref int iterations, ref float initialTemp, ref int bestDistance)
        {
            sol = bestSolution;
            coolFactor = mult;
            iterations = dimension;
            initialTemp = initTemp;
            bestDistance = distance;
        }

        public void setRandSeed(int n)
        {
            rand = new Random(n);
        }
    }
}

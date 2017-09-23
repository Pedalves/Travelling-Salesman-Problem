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
        float temp = 400;

        //Temperature cooldown multiplier
        float mult = 0.999f;
        
        //Current solution
        List<int> current;

        //Best solution
        List<int> bestSolution;

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

            return true;
        }

        /// <summary>
        /// Calculates the TSP solution
        /// </summary>
        /// <returns>the solution</returns>
        public List<int> CalculateTSP()
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
                temp = 400;
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
            Console.WriteLine("\nPeso: " + CalculateDistance(bestSolution));

            return bestSolution;
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
                //Clones the current solution
                foreach(int n in current)
                {
                    newSolution.Add(n);
                }

                //Perfoms a swap
                int i;
                int j;
                do
                {
                    i = rand.Next(dimension);
                    j = rand.Next(dimension);
                } while (i == j);

                int temp = newSolution[i];
                newSolution[i] = newSolution[j];
                newSolution[j] = temp;

                //Console.WriteLine("Swap " + i + " - " + j);
                //Console.WriteLine("current");
                //foreach (int n in current)
                //{
                //    Console.Write(n + " ");
                //}
                //Console.WriteLine("new");
                //foreach (int n in newSolution)
                //{
                //    Console.Write(n + " ");
                //}

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
    }
}

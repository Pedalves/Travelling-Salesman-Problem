using System;
using System.Collections.Generic;

namespace T1IA
{
    class Program
    {
        static void Main(string[] args)
        {
            string path = "resources/gr17.tsp";
            List<int> solution = null;

            //Creates a new simulated annealing class
            SimulatedAnnealing sa = new SimulatedAnnealing();

            //Read the file at given path
            if (sa.ReadFile(path))
            {
                //If successfull, calculates the solution

                //Start timer
                var timer = System.Diagnostics.Stopwatch.StartNew();

                solution = sa.CalculateTSP();

                //Stop timer
                timer.Stop();

                var executionTime = timer.ElapsedMilliseconds;

                Console.WriteLine("Tempo de execucao: " + executionTime + "ms");
            }
            else
            {
                Console.WriteLine("Error: read fail\n");
            }

            if(solution == null)
            {
                Console.WriteLine("Error: solution null\n");
            }
            
            if (System.Diagnostics.Debugger.IsAttached)
            {
                Console.ReadLine();
            }
        }
    }
}

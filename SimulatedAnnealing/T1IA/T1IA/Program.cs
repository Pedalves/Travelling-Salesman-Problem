using System;
using System.Collections.Generic;
using System.IO;

namespace T1IA
{
    class Program
    {
        static void Main(string[] args)
        {
            //gr17
            //gr21
            //gr24
            //hk48
            //si175
            string path = "resources/si175.tsp";
            List<int> solution = null;
            float coolFactor = 0;
            int iterations = 0;
            float initialTemp = 0;
            int bestDistance = 0;
            int seed = 0;

            //Creates a new simulated annealing class
            SimulatedAnnealing sa = new SimulatedAnnealing();


            if (args.Length > 0)
            {
                bool result = Int32.TryParse(args[0], out seed);
                if (result)
                {
                    sa.setRandSeed(seed);

                    Console.WriteLine("Usando seed: " + seed);
                }
            }

            //Read the file at given path
            if (sa.ReadFile(path))
            {
                //If successfull, calculates the solution

                //Start timer
                var timer = System.Diagnostics.Stopwatch.StartNew();

                sa.CalculateTSP();

                //Stop timer
                timer.Stop();

                var executionTime = timer.ElapsedMilliseconds;

                Console.WriteLine("Tempo de execucao: " + executionTime + "ms");
            }
            else
            {
                Console.WriteLine("Error: read fail\n");
            }

            sa.getParameters(ref solution, ref coolFactor, ref iterations, ref initialTemp, ref bestDistance);

            string[] lines = { "Solution: ", "Cooling factor: ", "Number of iterations: ", "Initial temperature: ", "Distance: ", "Seed: " };
            foreach(int n in solution)
            {
                lines[0] += n + " - ";
            }
            lines[1] += coolFactor;
            lines[2] += iterations;
            lines[3] += initialTemp;
            lines[4] += bestDistance;
            if(seed == 0)
            {
                lines[5] += "Valor Default do método (valor de semente padrão dependente de tempo). Para usar outro valor, passe como primeiro parametro para o executavel";
            }
            else
            {
                lines[5] += seed;
            }
            File.WriteAllLines(@"si175C#.sol", lines);

            if (System.Diagnostics.Debugger.IsAttached)
            {
                Console.ReadLine();
            }
        }
    }
}

using System;
using OpenTK;
using OpenTK.Graphics;
using OpenTK.Graphics.OpenGL4;

namespace OpenTKSamples
{
    public class Program : OpenTK.GameWindow
    {
        [STAThread]
        static void Main()
        {
            var sample = new Sample004(800, 600);
            sample.Run();
        }
    }
}

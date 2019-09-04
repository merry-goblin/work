using System;
using OpenTK;
using OpenTK.Graphics;
using OpenTK.Graphics.OpenGL4;

namespace OpenTKSamples
{
    public class Sample003 : OpenTK.GameWindow
    {
        // A simple vertex shader possible. Just passes through the position vector.
        const string VertexShaderSource = @"
            #version 330
            layout(location = 0) in vec3 positionAttribute;
            layout(location = 1) in vec3 colorAttribute;
            out vec3 vsColor;

            void main(void)
            {
                gl_Position = vec4(positionAttribute, 1.0);
                vsColor = colorAttribute;
            }
        ";

        // A simple fragment shader. Just a constant red color.
        const string FragmentShaderSource = @"
            #version 330
            in vec3 vsColor;
            out vec4 outputColor;

            void main(void)
            {
                outputColor = vec4(vsColor, 1.0);
            }
        ";

        // Points of a triangle in normalized device coordinates.
        readonly float[] Points = new float[] {
            // X, Y, Z, W
             0.5f, -0.5f, 0.0f,  1.0f, 0.0f, 0.0f,
            -0.5f, -0.5f, 0.0f,  0.0f, 1.0f, 0.0f,
             0.0f,  0.5f, 0.0f,  0.0f, 0.0f, 1.0f,
        };

        int VertexShader;
        int FragmentShader;
        int ShaderProgram;
        int VertexBufferObject;
        int VertexArrayObject;

        public Sample003(int width, int height) : base(width, height)
        {

        }

        protected override void OnLoad(EventArgs e)
        {
            // Load and compile the source of the vertex shader
            VertexShader = GL.CreateShader(ShaderType.VertexShader);
            GL.ShaderSource(VertexShader, VertexShaderSource);
            GL.CompileShader(VertexShader);

            // Load and compile the source of the fragment shader
            FragmentShader = GL.CreateShader(ShaderType.FragmentShader);
            GL.ShaderSource(FragmentShader, FragmentShaderSource);
            GL.CompileShader(FragmentShader);

            // Create the shader program, attach the vertex and fragment shaders and link the program.
            ShaderProgram = GL.CreateProgram();
            GL.AttachShader(ShaderProgram, VertexShader);
            GL.AttachShader(ShaderProgram, FragmentShader);
            GL.LinkProgram(ShaderProgram);

            // VBO
            VertexBufferObject = GL.GenBuffer();
            GL.BindBuffer(BufferTarget.ArrayBuffer, VertexBufferObject);
            GL.BufferData(BufferTarget.ArrayBuffer, Points.Length * sizeof(float), Points, BufferUsageHint.StaticDraw);

            // VAO
            VertexArrayObject = GL.GenVertexArray();
            GL.BindVertexArray(VertexArrayObject);

            // Position attribute
            var positionLocation = GL.GetAttribLocation(ShaderProgram, "positionAttribute");
            if (positionLocation != -1)
            {
                GL.VertexAttribPointer(positionLocation, 3, VertexAttribPointerType.Float, false, 6 * sizeof(float), 0);
                GL.EnableVertexAttribArray(positionLocation);
            }

            // Color attribute
            var colorLocation = GL.GetAttribLocation(ShaderProgram, "colorAttribute");
            if (colorLocation != -1)
            {
                GL.VertexAttribPointer(colorLocation, 3, VertexAttribPointerType.Float, false, 6 * sizeof(float), 3 * sizeof(float));
                GL.EnableVertexAttribArray(colorLocation);
            }

            // Set the clear color to blue
            GL.ClearColor(0.2f, 0.2f, 0.2f, 0.0f);

            base.OnLoad(e);
        }

        protected override void OnUnload(EventArgs e)
        {
            // Unbind all the resources by binding the targets to 0/null.
            GL.BindBuffer(BufferTarget.ArrayBuffer, 0);
            GL.BindVertexArray(0);
            GL.UseProgram(0);

            // Delete all the resources.
            GL.DeleteBuffer(VertexBufferObject);
            GL.DeleteVertexArray(VertexArrayObject);
            GL.DeleteProgram(ShaderProgram);
            GL.DeleteShader(FragmentShader);
            GL.DeleteShader(VertexShader);

            base.OnUnload(e);
        }

        protected override void OnResize(EventArgs e)
        {
            // Resize the viewport to match the window size.
            GL.Viewport(0, 0, Width, Height);
            base.OnResize(e);
        }

        protected override void OnRenderFrame(FrameEventArgs e)
        {
            // Clear the color buffer.
            GL.Clear(ClearBufferMask.ColorBufferBit);

            // Bind the VBO
            GL.BindBuffer(BufferTarget.ArrayBuffer, VertexBufferObject);
            // Bind the VAO
            GL.BindVertexArray(VertexArrayObject);
            // Use/Bind the program
            GL.UseProgram(ShaderProgram);
            // This draws the triangle.
            GL.DrawArrays(PrimitiveType.Triangles, 0, 3);

            // Swap the front/back buffers so what we just rendered to the back buffer is displayed in the window.
            Context.SwapBuffers();
            base.OnRenderFrame(e);
        }
    }
}

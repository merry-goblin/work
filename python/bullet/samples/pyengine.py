
import pygame
import pybullet as p
from numpy import float32
from OpenGL.GL import *
from vecutils import *
farray = float32

class URDFManager:

    def __init__(self, physicsClientId):
        self.physicsClientId = physicsClientId
        self.visualShapes = []

    def add(self, file, pos, orn):
        self.file = file
        self.pos = pos
        self.orn = orn
        
        multiBodyId = p.loadURDF(file)
        return multiBodyId


class WavefrontVisualiser:

    def __init__(self, obj, pos, orn=None):
        material = obj.materials['Material']
        self.vertex_format = material.vertex_format
        self.vertices = farray(material.vertices)
        self.texture = material.texture
        self.uTexture = None
        self.pos = pos
        self.orn = orn

        if self.vertex_format == "T2F_N3F_V3F":
            self.initT2F_N3F_V3F()
        elif self.vertex_format == "T2F_V3F":
            self.initT2F_V3F()

    def initT2F_N3F_V3F(self):
        self.hasNormals = True
        self.hasTextures = True
        self.hasColors = False

        self.rowSize = 8
        self.positionSize = 3
        self.positionStart = 5
        self.normalSize = 3
        self.normalStart = 2
        self.textureSize = 3
        self.textureStart = 0
        
    def initT2F_V3F(self):
        self.hasNormals = False
        self.hasTextures = True
        self.hasColors = False

        self.rowSize = 5
        self.positionSize = 3
        self.positionStart = 2
        self.textureSize = 3
        self.textureStart = 0
        

    def updatePosAndOrn(self, pos, orn):
        self.pos = pos
        self.orn = orn

    def prepare(self, shaderProgram):
        self.vao = glGenVertexArrays(1)
        vbo = glGenBuffers(1)

        glBindVertexArray(self.vao)

        # Bind the Vertex Buffer
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(self.vertices), self.vertices, GL_STATIC_DRAW)

        # Configure vertex attributes

        # - Position attribute
        attrPositionIndex = glGetAttribLocation(shaderProgram, 'attrPosition')
        if (attrPositionIndex != -1):
            glVertexAttribPointer(attrPositionIndex, self.positionSize, GL_FLOAT, GL_FALSE, self.rowSize * ctypes.sizeof(ctypes.c_float), ctypes.c_void_p(self.positionStart * ctypes.sizeof(ctypes.c_float)))
            glEnableVertexAttribArray(attrPositionIndex)

        # - Texture attribute
        if (self.hasTextures):
            attrTexCoordIndex = glGetAttribLocation(shaderProgram, 'attrTexCoords')
            if (attrTexCoordIndex != -1):
                glVertexAttribPointer(attrTexCoordIndex, self.textureSize, GL_FLOAT, GL_FALSE, self.rowSize * ctypes.sizeof(ctypes.c_float), ctypes.c_void_p(self.textureStart * ctypes.sizeof(ctypes.c_float)))
                glEnableVertexAttribArray(attrTexCoordIndex)

        self.uTexture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.uTexture)
        # Set the texture wrapping parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT) # Set texture wrapping to GL_REPEAT (default wrapping method)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        # Set texture filtering parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        image = pygame.image.load(self.texture.path).convert_alpha()
        imageData = pygame.image.tostring(image, 'RGBA', 1)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.get_width(), image.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, imageData)
        glGenerateMipmap(GL_TEXTURE_2D)

        # Unbind the VAO
        glBindVertexArray(0)
        
        # Unbind attribute buffer
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        if (attrPositionIndex != -1):
            glDisableVertexAttribArray(attrPositionIndex)
        if (attrTexCoordIndex != -1):
            glDisableVertexAttribArray(attrTexCoordIndex)

    def draw(self, shaderProgram, time):

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.uTexture)

        glUseProgram(shaderProgram)

        pMatrix = PerspectiveMatrix(45, 1.0 * 800/600, 0.1, 100)

        lMatrix = LookAtMatrix(vec3(-12.0, 12.0, 10.0), (0, 0, 2), (0, 0, 1))

        if self.orn is not None:
            orn9x1Matrix = p.getMatrixFromQuaternion(self.orn)
            orn4x4Matrix = getA4x4MatrixWithA9x1Matrix(orn9x1Matrix)
        else:
            orn4x4Matrix = IdentityMatrix()

        # Matrix
        #objectMatrix = TranslationMatrix(sin(time), 0, 0) @ RotationMatrix(sin(time)*90, (1,1,1))
        objectMatrix = TranslationMatrix(self.pos) @ orn4x4Matrix
        attrMatrixIndex = glGetUniformLocation(shaderProgram, 'matrix')
        glUniformMatrix4fv(attrMatrixIndex, 1, True, pMatrix @ lMatrix @ objectMatrix)

        glBindVertexArray(self.vao)
        #glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_INT, ctypes.c_void_p(0))
        glDrawArrays(GL_TRIANGLES, 0, len(self.vertices)//3)

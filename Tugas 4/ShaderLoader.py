from OpenGL.GL import *

def load_shader(shader_file):
    shader_source = ""
    with open(shader_file) as f:
        shader_source = f.read()
    f.close()
    return str.encode(shader_source)

def compile_shader(vs_file, fs_file):
    vert_shader = load_shader(vs_file)
    frag_shader = load_shader(fs_file)

    shader = glCreateProgram()
    vs = glCreateShader(GL_VERTEX_SHADER)
    glShaderSource(vs, [vert_shader])
    glCompileShader(vs)
    if not glGetShaderiv(vs, GL_COMPILE_STATUS):
        raise Exception('failed to compile shader "%s":\n%s' % (vs, glGetShaderInfoLog(vs).decode()))
    
    glAttachShader(shader, vs)

    fs = glCreateShader(GL_FRAGMENT_SHADER)
    glShaderSource(fs, [frag_shader])
    glCompileShader(fs)
    if not glGetShaderiv(fs, GL_COMPILE_STATUS):
        raise Exception('failed to compile shader "%s":\n%s' % (fs, glGetShaderInfoLog(fs).decode()))
    glAttachShader(shader, fs)

    glLinkProgram(shader)
    glValidateProgram(shader)
    glDeleteShader(vs)
    glDeleteShader(fs)
    
    return shader
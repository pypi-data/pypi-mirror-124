#include <Python.h>
#include <structmember.h>

#if defined(_WIN32) || defined(_WIN64)
#define GLAPI __stdcall
#else
#define GLAPI
#endif

#define GL_DEPTH_BUFFER_BIT 0x00000100
#define GL_STENCIL_BUFFER_BIT 0x00000400
#define GL_COLOR_BUFFER_BIT 0x00004000
#define GL_POINTS 0x0000
#define GL_LINES 0x0001
#define GL_LINE_LOOP 0x0002
#define GL_LINE_STRIP 0x0003
#define GL_TRIANGLES 0x0004
#define GL_TRIANGLE_STRIP 0x0005
#define GL_TRIANGLE_FAN 0x0006
#define GL_FRONT 0x0404
#define GL_BACK 0x0405
#define GL_CULL_FACE 0x0B44
#define GL_DEPTH_TEST 0x0B71
#define GL_STENCIL_TEST 0x0B90
#define GL_BLEND 0x0BE2
#define GL_TEXTURE_2D 0x0DE1
#define GL_TEXTURE_BORDER_COLOR 0x1004
#define GL_BYTE 0x1400
#define GL_UNSIGNED_BYTE 0x1401
#define GL_SHORT 0x1402
#define GL_UNSIGNED_SHORT 0x1403
#define GL_INT 0x1404
#define GL_UNSIGNED_INT 0x1405
#define GL_FLOAT 0x1406
#define GL_STENCIL_INDEX 0x1901
#define GL_DEPTH_COMPONENT 0x1902
#define GL_RED 0x1903
#define GL_RGBA 0x1908
#define GL_VENDOR 0x1F00
#define GL_RENDERER 0x1F01
#define GL_VERSION 0x1F02
#define GL_NEAREST 0x2600
#define GL_LINEAR 0x2601
#define GL_TEXTURE_MAG_FILTER 0x2800
#define GL_TEXTURE_MIN_FILTER 0x2801
#define GL_TEXTURE_WRAP_S 0x2802
#define GL_TEXTURE_WRAP_T 0x2803
#define GL_POLYGON_OFFSET_POINT 0x2A01
#define GL_POLYGON_OFFSET_LINE 0x2A02
#define GL_POLYGON_OFFSET_FILL 0x8037
#define GL_RGBA8 0x8058
#define GL_TEXTURE_WRAP_R 0x8072
#define GL_BGRA 0x80E1
#define GL_TEXTURE_MIN_LOD 0x813A
#define GL_TEXTURE_MAX_LOD 0x813B
#define GL_TEXTURE_BASE_LEVEL 0x813C
#define GL_TEXTURE_MAX_LEVEL 0x813D
#define GL_TEXTURE0 0x84C0
#define GL_TEXTURE_CUBE_MAP 0x8513
#define GL_TEXTURE_CUBE_MAP_POSITIVE_X 0x8515
#define GL_DEPTH_COMPONENT16 0x81A5
#define GL_DEPTH_COMPONENT24 0x81A6
#define GL_TEXTURE_COMPARE_MODE 0x884C
#define GL_TEXTURE_COMPARE_FUNC 0x884D
#define GL_ARRAY_BUFFER 0x8892
#define GL_ELEMENT_ARRAY_BUFFER 0x8893
#define GL_STATIC_DRAW 0x88E4
#define GL_DYNAMIC_DRAW 0x88E8
#define GL_MAX_TEXTURE_IMAGE_UNITS 0x8872
#define GL_FRAGMENT_SHADER 0x8B30
#define GL_VERTEX_SHADER 0x8B31
#define GL_COMPILE_STATUS 0x8B81
#define GL_LINK_STATUS 0x8B82
#define GL_INFO_LOG_LENGTH 0x8B84
#define GL_ACTIVE_UNIFORMS 0x8B86
#define GL_ACTIVE_ATTRIBUTES 0x8B89
#define GL_SRGB8_ALPHA8 0x8C43
#define GL_RGBA32F 0x8814
#define GL_RGBA16F 0x881A
#define GL_TEXTURE_2D_ARRAY 0x8C1A
#define GL_RGBA32UI 0x8D70
#define GL_RGBA16UI 0x8D76
#define GL_RGBA8UI 0x8D7C
#define GL_RGBA32I 0x8D82
#define GL_RGBA16I 0x8D88
#define GL_RGBA8I 0x8D8E
#define GL_DEPTH_COMPONENT32F 0x8CAC
#define GL_DEPTH_STENCIL_ATTACHMENT 0x821A
#define GL_DEPTH_STENCIL 0x84F9
#define GL_DEPTH24_STENCIL8 0x88F0
#define GL_READ_FRAMEBUFFER 0x8CA8
#define GL_DRAW_FRAMEBUFFER 0x8CA9
#define GL_COLOR_ATTACHMENT0 0x8CE0
#define GL_DEPTH_ATTACHMENT 0x8D00
#define GL_STENCIL_ATTACHMENT 0x8D20
#define GL_FRAMEBUFFER 0x8D40
#define GL_RENDERBUFFER 0x8D41
#define GL_STENCIL_INDEX8 0x8D48
#define GL_HALF_FLOAT 0x140B
#define GL_MAP_READ_BIT 0x0001
#define GL_MAP_WRITE_BIT 0x0002
#define GL_MAP_INVALIDATE_RANGE_BIT 0x0004
#define GL_RG 0x8227
#define GL_R8 0x8229
#define GL_RG8 0x822B
#define GL_R16F 0x822D
#define GL_R32F 0x822E
#define GL_RG16F 0x822F
#define GL_RG32F 0x8230
#define GL_R8I 0x8231
#define GL_R8UI 0x8232
#define GL_R16I 0x8233
#define GL_R16UI 0x8234
#define GL_R32I 0x8235
#define GL_R32UI 0x8236
#define GL_RG8I 0x8237
#define GL_RG8UI 0x8238
#define GL_RG16I 0x8239
#define GL_RG16UI 0x823A
#define GL_RG32I 0x823B
#define GL_RG32UI 0x823C
#define GL_R8_SNORM 0x8F94
#define GL_RG8_SNORM 0x8F95
#define GL_RGBA8_SNORM 0x8F97
#define GL_PRIMITIVE_RESTART 0x8F9D
#define GL_UNIFORM_BUFFER 0x8A11
#define GL_ACTIVE_UNIFORM_BLOCKS 0x8A36
#define GL_UNIFORM_BLOCK_DATA_SIZE 0x8A40

typedef void (GLAPI * glActiveTextureProc)(unsigned int texture);
typedef void (GLAPI * glAttachShaderProc)(unsigned int program, unsigned int shader);
typedef void (GLAPI * glBindBufferProc)(unsigned int target, unsigned int buffer);
typedef void (GLAPI * glBindBufferRangeProc)(unsigned int target, unsigned int index, unsigned int buffer, long long int offset, long long int size);
typedef void (GLAPI * glBindFramebufferProc)(unsigned int target, unsigned int framebuffer);
typedef void (GLAPI * glBindRenderbufferProc)(unsigned int target, unsigned int renderbuffer);
typedef void (GLAPI * glBindSamplerProc)(unsigned int unit, unsigned int sampler);
typedef void (GLAPI * glBindTextureProc)(unsigned int target, unsigned int texture);
typedef void (GLAPI * glBindVertexArrayProc)(unsigned int array);
typedef void (GLAPI * glBlendFuncSeparateProc)(unsigned int sfactorRGB, unsigned int dfactorRGB, unsigned int sfactorAlpha, unsigned int dfactorAlpha);
typedef void (GLAPI * glBlitFramebufferProc)(int srcX0, int srcY0, int srcX1, int srcY1, int dstX0, int dstY0, int dstX1, int dstY1, unsigned int mask, unsigned int filter);
typedef void (GLAPI * glBufferDataProc)(unsigned int target, long long int size, const void * data, unsigned int usage);
typedef void (GLAPI * glBufferSubDataProc)(unsigned int target, long long int offset, long long int size, const void * data);
typedef void (GLAPI * glClearProc)(unsigned int mask);
typedef void (GLAPI * glClearColorProc)(float red, float green, float blue, float alpha);
typedef void (GLAPI * glClearDepthProc)(double depth);
typedef void (GLAPI * glClearStencilProc)(int s);
typedef void (GLAPI * glColorMaskiProc)(unsigned int index, unsigned char r, unsigned char g, unsigned char b, unsigned char a);
typedef void (GLAPI * glCompileShaderProc)(unsigned int shader);
typedef unsigned int (GLAPI * glCreateProgramProc)();
typedef unsigned int (GLAPI * glCreateShaderProc)(unsigned int type);
typedef void (GLAPI * glCullFaceProc)(unsigned int mode);
typedef void (GLAPI * glDeleteBuffersProc)(int n, const unsigned int * buffers);
typedef void (GLAPI * glDeleteFramebuffersProc)(int n, const unsigned int * framebuffers);
typedef void (GLAPI * glDeleteProgramProc)(unsigned int program);
typedef void (GLAPI * glDeleteRenderbufferspProc)(int n, const unsigned int * renderbuffers);
typedef void (GLAPI * glDeleteSamplersProc)(int count, const unsigned int * samplers);
typedef void (GLAPI * glDeleteShaderProc)(unsigned int shader);
typedef void (GLAPI * glDeleteTexturesProc)(int n, const unsigned int * textures);
typedef void (GLAPI * glDeleteVertexArraysProc)(int n, const unsigned int * arrays);
typedef void (GLAPI * glDepthFuncProc)(unsigned int func);
typedef void (GLAPI * glDepthMaskProc)(unsigned char flag);
typedef void (GLAPI * glDisableProc)(unsigned int cap);
typedef void (GLAPI * glDisableiProc)(unsigned int target, unsigned int index);
typedef void (GLAPI * glDrawArraysInstancedProc)(unsigned int mode, int first, int count, int instancecount);
typedef void (GLAPI * glDrawBuffersProc)(int n, const unsigned int * bufs);
typedef void (GLAPI * glDrawElementsInstancedProc)(unsigned int mode, int count, unsigned int type, const void * indices, int instancecount);
typedef void (GLAPI * glEnableProc)(unsigned int cap);
typedef void (GLAPI * glEnableiProc)(unsigned int target, unsigned int index);
typedef void (GLAPI * glEnableVertexAttribArrayProc)(unsigned int index);
typedef void (GLAPI * glFramebufferRenderbufferProc)(unsigned int target, unsigned int attachment, unsigned int renderbuffertarget, unsigned int renderbuffer);
typedef void (GLAPI * glFramebufferTexture2DProc)(unsigned int target, unsigned int attachment, unsigned int textarget, unsigned int texture, int level);
typedef void (GLAPI * glFrontFaceProc)(unsigned int mode);
typedef void (GLAPI * glGenBuffersProc)(int n, unsigned int * buffers);
typedef void (GLAPI * glGenerateMipmapProc)(unsigned int target);
typedef void (GLAPI * glGenFramebuffersProc)(int n, unsigned int * framebuffers);
typedef void (GLAPI * glGenRenderbuffersProc)(int n, unsigned int * renderbuffers);
typedef void (GLAPI * glGenSamplersProc)(int count, unsigned int * samplers);
typedef void (GLAPI * glGenTexturesProc)(int n, unsigned int * textures);
typedef void (GLAPI * glGenVertexArraysProc)(int n, unsigned int * arrays);
typedef void (GLAPI * glGetActiveAttribProc)(unsigned int program, unsigned int index, int bufSize, int * length, int * size, unsigned int * type, char * name);
typedef void (GLAPI * glGetActiveUniformProc)(unsigned int program, unsigned int index, int bufSize, int * length, int * size, unsigned int * type, char * name);
typedef void (GLAPI * glGetActiveUniformBlockivProc)(unsigned int program, unsigned int uniformBlockIndex, unsigned int pname, int * params);
typedef void (GLAPI * glGetActiveUniformBlockNameProc)(unsigned int program, unsigned int uniformBlockIndex, int bufSize, int * length, char * uniformBlockName);
typedef int (GLAPI * glGetAttribLocationProc)(unsigned int program, const char * name);
typedef unsigned int (GLAPI * glGetErrorProc)();
typedef void (GLAPI * glGetIntegervProc)(unsigned int pname, int * data);
typedef void (GLAPI * glGetProgramInfoLogProc)(unsigned int program, int bufSize, int * length, char * infoLog);
typedef void (GLAPI * glGetProgramivProc)(unsigned int program, unsigned int pname, int * params);
typedef void (GLAPI * glGetShaderInfoLogProc)(unsigned int shader, int bufSize, int * length, char * infoLog);
typedef void (GLAPI * glGetShaderivProc)(unsigned int shader, unsigned int pname, int * params);
typedef const unsigned char * (GLAPI * glGetStringProc)(unsigned int name);
typedef unsigned int (GLAPI * glGetUniformBlockIndexProc)(unsigned int program, const char * uniformBlockName);
typedef int (GLAPI * glGetUniformLocationProc)(unsigned int program, const char * name);
typedef void (GLAPI * glLineWidthProc)(float width);
typedef void (GLAPI * glLinkProgramProc)(unsigned int program);
typedef void * (GLAPI * glMapBufferRangeProc)(unsigned int target, long long int offset, long long int length, unsigned int access);
typedef void (GLAPI * glPointSizeProc)(float size);
typedef void (GLAPI * glPolygonOffsetProc)(float factor, float units);
typedef void (GLAPI * glPrimitiveRestartIndexProc)(unsigned int index);
typedef void (GLAPI * glReadBufferProc)(unsigned int src);
typedef void (GLAPI * glReadPixelsProc)(int x, int y, int width, int height, unsigned int format, unsigned int type, void * pixels);
typedef void (GLAPI * glRenderbufferStorageMultisampleProc)(unsigned int target, int samples, unsigned int internalformat, int width, int height);
typedef void (GLAPI * glSamplerParameterfProc)(unsigned int sampler, unsigned int pname, float param);
typedef void (GLAPI * glSamplerParameterfvProc)(unsigned int sampler, unsigned int pname, const float * param);
typedef void (GLAPI * glSamplerParameteriProc)(unsigned int sampler, unsigned int pname, int param);
typedef void (GLAPI * glShaderSourceProc)(unsigned int shader, int count, const char * const * string, const int * length);
typedef void (GLAPI * glStencilFuncSeparateProc)(unsigned int face, unsigned int func, int ref, unsigned int mask);
typedef void (GLAPI * glStencilMaskSeparateProc)(unsigned int face, unsigned int mask);
typedef void (GLAPI * glStencilOpSeparateProc)(unsigned int face, unsigned int sfail, unsigned int dpfail, unsigned int dppass);
typedef void (GLAPI * glTexImage2DProc)(unsigned int target, int level, int internalformat, int width, int height, int border, unsigned int format, unsigned int type, const void * pixels);
typedef void (GLAPI * glTexImage3DProc)(unsigned int target, int level, int internalformat, int width, int height, int depth, int border, unsigned int format, unsigned int type, const void * pixels);
typedef void (GLAPI * glTexParameteriProc)(unsigned int target, unsigned int pname, int param);
typedef void (GLAPI * glTexSubImage2DProc)(unsigned int target, int level, int xoffset, int yoffset, int width, int height, unsigned int format, unsigned int type, const void * pixels);
typedef void (GLAPI * glTexSubImage3DProc)(unsigned int target, int level, int xoffset, int yoffset, int zoffset, int width, int height, int depth, unsigned int format, unsigned int type, const void * pixels);
typedef void (GLAPI * glUniform1iProc)(int location, int v0);
typedef void (GLAPI * glUniformBlockBindingProc)(unsigned int program, unsigned int uniformBlockIndex, unsigned int uniformBlockBinding);
typedef unsigned char (GLAPI * glUnmapBufferProc)(unsigned int target);
typedef void (GLAPI * glUseProgramProc)(unsigned int program);
typedef void (GLAPI * glVertexAttribDivisorProc)(unsigned int index, unsigned int divisor);
typedef void (GLAPI * glVertexAttribIPointerProc)(unsigned int index, int size, unsigned int type, int stride, const void * pointer);
typedef void (GLAPI * glVertexAttribPointerProc)(unsigned int index, int size, unsigned int type, unsigned char normalized, int stride, const void * pointer);
typedef void (GLAPI * glViewportProc)(int x, int y, int width, int height);

const int MAX_ATTACHMENTS = 16;
const int MAX_UNIFORM_BUFFER_BINDINGS = 16;
const int MAX_SAMPLER_BINDINGS = 64;

struct GLMethods {
    glActiveTextureProc ActiveTexture;
    glAttachShaderProc AttachShader;
    glBindBufferProc BindBuffer;
    glBindBufferRangeProc BindBufferRange;
    glBindFramebufferProc BindFramebuffer;
    glBindRenderbufferProc BindRenderbuffer;
    glBindSamplerProc BindSampler;
    glBindTextureProc BindTexture;
    glBindVertexArrayProc BindVertexArray;
    glBlendFuncSeparateProc BlendFuncSeparate;
    glBlitFramebufferProc BlitFramebuffer;
    glBufferDataProc BufferData;
    glBufferSubDataProc BufferSubData;
    glClearProc Clear;
    glClearColorProc ClearColor;
    glClearDepthProc ClearDepth;
    glClearStencilProc ClearStencil;
    glColorMaskiProc ColorMaski;
    glCompileShaderProc CompileShader;
    glCreateProgramProc CreateProgram;
    glCreateShaderProc CreateShader;
    glCullFaceProc CullFace;
    glDeleteBuffersProc DeleteBuffers;
    glDeleteFramebuffersProc DeleteFramebuffers;
    glDeleteProgramProc DeleteProgram;
    glDeleteRenderbufferspProc DeleteRenderbuffersp;
    glDeleteSamplersProc DeleteSamplers;
    glDeleteShaderProc DeleteShader;
    glDeleteTexturesProc DeleteTextures;
    glDeleteVertexArraysProc DeleteVertexArrays;
    glDepthFuncProc DepthFunc;
    glDepthMaskProc DepthMask;
    glDisableProc Disable;
    glDisableiProc Disablei;
    glDrawArraysInstancedProc DrawArraysInstanced;
    glDrawBuffersProc DrawBuffers;
    glDrawElementsInstancedProc DrawElementsInstanced;
    glEnableProc Enable;
    glEnableiProc Enablei;
    glEnableVertexAttribArrayProc EnableVertexAttribArray;
    glFramebufferRenderbufferProc FramebufferRenderbuffer;
    glFramebufferTexture2DProc FramebufferTexture2D;
    glFrontFaceProc FrontFace;
    glGenBuffersProc GenBuffers;
    glGenerateMipmapProc GenerateMipmap;
    glGenFramebuffersProc GenFramebuffers;
    glGenRenderbuffersProc GenRenderbuffers;
    glGenSamplersProc GenSamplers;
    glGenTexturesProc GenTextures;
    glGenVertexArraysProc GenVertexArrays;
    glGetActiveAttribProc GetActiveAttrib;
    glGetActiveUniformProc GetActiveUniform;
    glGetActiveUniformBlockivProc GetActiveUniformBlockiv;
    glGetActiveUniformBlockNameProc GetActiveUniformBlockName;
    glGetAttribLocationProc GetAttribLocation;
    glGetErrorProc GetError;
    glGetIntegervProc GetIntegerv;
    glGetProgramInfoLogProc GetProgramInfoLog;
    glGetProgramivProc GetProgramiv;
    glGetShaderInfoLogProc GetShaderInfoLog;
    glGetShaderivProc GetShaderiv;
    glGetStringProc GetString;
    glGetUniformBlockIndexProc GetUniformBlockIndex;
    glGetUniformLocationProc GetUniformLocation;
    glLineWidthProc LineWidth;
    glLinkProgramProc LinkProgram;
    glMapBufferRangeProc MapBufferRange;
    glPointSizeProc PointSize;
    glPolygonOffsetProc PolygonOffset;
    glPrimitiveRestartIndexProc PrimitiveRestartIndex;
    glReadBufferProc ReadBuffer;
    glReadPixelsProc ReadPixels;
    glRenderbufferStorageMultisampleProc RenderbufferStorageMultisample;
    glSamplerParameterfProc SamplerParameterf;
    glSamplerParameterfvProc SamplerParameterfv;
    glSamplerParameteriProc SamplerParameteri;
    glShaderSourceProc ShaderSource;
    glStencilFuncSeparateProc StencilFuncSeparate;
    glStencilMaskSeparateProc StencilMaskSeparate;
    glStencilOpSeparateProc StencilOpSeparate;
    glTexImage2DProc TexImage2D;
    glTexImage3DProc TexImage3D;
    glTexParameteriProc TexParameteri;
    glTexSubImage2DProc TexSubImage2D;
    glTexSubImage3DProc TexSubImage3D;
    glUniform1iProc Uniform1i;
    glUniformBlockBindingProc UniformBlockBinding;
    glUnmapBufferProc UnmapBuffer;
    glUseProgramProc UseProgram;
    glVertexAttribDivisorProc VertexAttribDivisor;
    glVertexAttribIPointerProc VertexAttribIPointer;
    glVertexAttribPointerProc VertexAttribPointer;
    glViewportProc Viewport;
};

struct VertexFormat {
    int type;
    int size;
    int normalize;
    int integer;
};

struct ImageFormat {
    int internal_format;
    int format;
    int type;
    int components;
    int pixel_size;
    int attachment;
};

struct UniformBufferBinding {
    int buffer;
    int offset;
    int size;
};

struct SamplerBinding {
    int sampler;
    int target;
    int image;
};

struct DescriptorSetBuffers {
    PyObject_HEAD
    int buffers;
    UniformBufferBinding buffer[MAX_UNIFORM_BUFFER_BINDINGS];
};

struct DescriptorSetImages {
    PyObject_HEAD
    int samplers;
    SamplerBinding sampler[MAX_SAMPLER_BINDINGS];
};

struct StencilSettings {
    int fail_op;
    int pass_op;
    int depth_fail_op;
    int compare_op;
    int compare_mask;
    int write_mask;
    int reference;
};

VertexFormat get_vertex_format(const char * format) {
    if (!strcmp(format, "uint8x2")) return {GL_UNSIGNED_BYTE, 2, false, true};
    if (!strcmp(format, "uint8x4")) return {GL_UNSIGNED_BYTE, 4, false, true};
    if (!strcmp(format, "sint8x2")) return {GL_BYTE, 2, false, true};
    if (!strcmp(format, "sint8x4")) return {GL_BYTE, 4, false, true};
    if (!strcmp(format, "unorm8x2")) return {GL_UNSIGNED_BYTE, 2, true, false};
    if (!strcmp(format, "unorm8x4")) return {GL_UNSIGNED_BYTE, 4, true, false};
    if (!strcmp(format, "snorm8x2")) return {GL_BYTE, 2, true, false};
    if (!strcmp(format, "snorm8x4")) return {GL_BYTE, 4, true, false};
    if (!strcmp(format, "uint16x2")) return {GL_UNSIGNED_SHORT, 2, false, true};
    if (!strcmp(format, "uint16x4")) return {GL_UNSIGNED_SHORT, 4, false, true};
    if (!strcmp(format, "sint16x2")) return {GL_SHORT, 2, false, true};
    if (!strcmp(format, "sint16x4")) return {GL_SHORT, 4, false, true};
    if (!strcmp(format, "unorm16x2")) return {GL_UNSIGNED_SHORT, 2, true, false};
    if (!strcmp(format, "unorm16x4")) return {GL_UNSIGNED_SHORT, 4, true, false};
    if (!strcmp(format, "snorm16x2")) return {GL_SHORT, 2, true, false};
    if (!strcmp(format, "snorm16x4")) return {GL_SHORT, 4, true, false};
    if (!strcmp(format, "float16x2")) return {GL_HALF_FLOAT, 2, false, false};
    if (!strcmp(format, "float16x4")) return {GL_HALF_FLOAT, 4, false, false};
    if (!strcmp(format, "float32")) return {GL_FLOAT, 1, false, false};
    if (!strcmp(format, "float32x2")) return {GL_FLOAT, 2, false, false};
    if (!strcmp(format, "float32x3")) return {GL_FLOAT, 3, false, false};
    if (!strcmp(format, "float32x4")) return {GL_FLOAT, 4, false, false};
    if (!strcmp(format, "uint32")) return {GL_UNSIGNED_INT, 1, false, true};
    if (!strcmp(format, "uint32x2")) return {GL_UNSIGNED_INT, 2, false, true};
    if (!strcmp(format, "uint32x3")) return {GL_UNSIGNED_INT, 3, false, true};
    if (!strcmp(format, "uint32x4")) return {GL_UNSIGNED_INT, 4, false, true};
    if (!strcmp(format, "sint32")) return {GL_INT, 1, false, true};
    if (!strcmp(format, "sint32x2")) return {GL_INT, 2, false, true};
    if (!strcmp(format, "sint32x3")) return {GL_INT, 3, false, true};
    if (!strcmp(format, "sint32x4")) return {GL_INT, 4, false, true};
    return {};
}

ImageFormat get_image_format(const char * format) {
    if (!strcmp(format, "r8unorm")) return {GL_R8, GL_RED, GL_UNSIGNED_BYTE, 1, 1, GL_COLOR_ATTACHMENT0};
    if (!strcmp(format, "rg8unorm")) return {GL_RG8, GL_RG, GL_UNSIGNED_BYTE, 2, 2, GL_COLOR_ATTACHMENT0};
    if (!strcmp(format, "rgba8unorm")) return {GL_RGBA8, GL_RGBA, GL_UNSIGNED_BYTE, 4, 4, GL_COLOR_ATTACHMENT0};
    if (!strcmp(format, "bgra8unorm")) return {GL_RGBA8, GL_BGRA, GL_UNSIGNED_BYTE, 4, 4, GL_COLOR_ATTACHMENT0};
    if (!strcmp(format, "r8snorm")) return {GL_R8_SNORM, GL_RED, GL_UNSIGNED_BYTE, 1, 1, GL_COLOR_ATTACHMENT0};
    if (!strcmp(format, "rg8snorm")) return {GL_RG8_SNORM, GL_RG, GL_UNSIGNED_BYTE, 2, 2, GL_COLOR_ATTACHMENT0};
    if (!strcmp(format, "rgba8snorm")) return {GL_RGBA8_SNORM, GL_RGBA, GL_UNSIGNED_BYTE, 4, 4, GL_COLOR_ATTACHMENT0};
    if (!strcmp(format, "r8uint")) return {GL_R8UI, GL_RED, GL_UNSIGNED_BYTE, 1, 1, GL_COLOR_ATTACHMENT0};
    if (!strcmp(format, "rg8uint")) return {GL_RG8UI, GL_RG, GL_UNSIGNED_BYTE, 2, 2, GL_COLOR_ATTACHMENT0};
    if (!strcmp(format, "rgba8uint")) return {GL_RGBA8UI, GL_RGBA, GL_UNSIGNED_BYTE, 4, 4, GL_COLOR_ATTACHMENT0};
    if (!strcmp(format, "r16uint")) return {GL_R16UI, GL_RED, GL_UNSIGNED_SHORT, 1, 2, GL_COLOR_ATTACHMENT0};
    if (!strcmp(format, "rg16uint")) return {GL_RG16UI, GL_RG, GL_UNSIGNED_SHORT, 2, 4, GL_COLOR_ATTACHMENT0};
    if (!strcmp(format, "rgba16uint")) return {GL_RGBA16UI, GL_RGBA, GL_UNSIGNED_SHORT, 4, 8, GL_COLOR_ATTACHMENT0};
    if (!strcmp(format, "r32uint")) return {GL_R32UI, GL_RED, GL_UNSIGNED_INT, 1, 4, GL_COLOR_ATTACHMENT0};
    if (!strcmp(format, "rg32uint")) return {GL_RG32UI, GL_RG, GL_UNSIGNED_INT, 2, 8, GL_COLOR_ATTACHMENT0};
    if (!strcmp(format, "rgba32uint")) return {GL_RGBA32UI, GL_RGBA, GL_UNSIGNED_INT, 4, 16, GL_COLOR_ATTACHMENT0};
    if (!strcmp(format, "r8sint")) return {GL_R8I, GL_RED, GL_BYTE, 1, 1, GL_COLOR_ATTACHMENT0};
    if (!strcmp(format, "rg8sint")) return {GL_RG8I, GL_RG, GL_BYTE, 2, 2, GL_COLOR_ATTACHMENT0};
    if (!strcmp(format, "rgba8sint")) return {GL_RGBA8I, GL_RGBA, GL_BYTE, 4, 4, GL_COLOR_ATTACHMENT0};
    if (!strcmp(format, "r16sint")) return {GL_R16I, GL_RED, GL_SHORT, 1, 2, GL_COLOR_ATTACHMENT0};
    if (!strcmp(format, "rg16sint")) return {GL_RG16I, GL_RG, GL_SHORT, 2, 4, GL_COLOR_ATTACHMENT0};
    if (!strcmp(format, "rgba16sint")) return {GL_RGBA16I, GL_RGBA, GL_SHORT, 4, 8, GL_COLOR_ATTACHMENT0};
    if (!strcmp(format, "r32sint")) return {GL_R32I, GL_RED, GL_INT, 1, 4, GL_COLOR_ATTACHMENT0};
    if (!strcmp(format, "rg32sint")) return {GL_RG32I, GL_RG, GL_INT, 2, 8, GL_COLOR_ATTACHMENT0};
    if (!strcmp(format, "rgba32sint")) return {GL_RGBA32I, GL_RGBA, GL_INT, 4, 16, GL_COLOR_ATTACHMENT0};
    if (!strcmp(format, "r16float")) return {GL_R16F, GL_RED, GL_FLOAT, 1, 2, GL_COLOR_ATTACHMENT0};
    if (!strcmp(format, "rg16float")) return {GL_RG16F, GL_RG, GL_FLOAT, 2, 4, GL_COLOR_ATTACHMENT0};
    if (!strcmp(format, "rgba16float")) return {GL_RGBA16F, GL_RGBA, GL_FLOAT, 4, 8, GL_COLOR_ATTACHMENT0};
    if (!strcmp(format, "r32float")) return {GL_R32F, GL_RED, GL_FLOAT, 1, 4, GL_COLOR_ATTACHMENT0};
    if (!strcmp(format, "rg32float")) return {GL_RG32F, GL_RG, GL_FLOAT, 2, 8, GL_COLOR_ATTACHMENT0};
    if (!strcmp(format, "rgba32float")) return {GL_RGBA32F, GL_RGBA, GL_FLOAT, 4, 16, GL_COLOR_ATTACHMENT0};
    if (!strcmp(format, "rgba8unorm-srgb")) return {GL_SRGB8_ALPHA8, GL_RGBA, GL_UNSIGNED_BYTE, 4, 4, GL_COLOR_ATTACHMENT0};
    if (!strcmp(format, "bgra8unorm-srgb")) return {GL_SRGB8_ALPHA8, GL_BGRA, GL_UNSIGNED_BYTE, 4, 4, GL_COLOR_ATTACHMENT0};
    if (!strcmp(format, "stencil8")) return {GL_STENCIL_INDEX8, GL_STENCIL_INDEX, GL_UNSIGNED_BYTE, 1, 1, GL_STENCIL_ATTACHMENT};
    if (!strcmp(format, "depth16unorm")) return {GL_DEPTH_COMPONENT16, GL_DEPTH_COMPONENT, GL_FLOAT, 1, 2, GL_DEPTH_ATTACHMENT};
    if (!strcmp(format, "depth24plus")) return {GL_DEPTH_COMPONENT24, GL_DEPTH_COMPONENT, GL_FLOAT, 1, 4, GL_DEPTH_ATTACHMENT};
    if (!strcmp(format, "depth24plus-stencil8")) return {GL_DEPTH24_STENCIL8, GL_DEPTH_STENCIL, GL_FLOAT, 2, 4, GL_DEPTH_STENCIL_ATTACHMENT};
    if (!strcmp(format, "depth32float")) return {GL_DEPTH_COMPONENT32F, GL_DEPTH_COMPONENT, GL_FLOAT, 1, 4, GL_DEPTH_ATTACHMENT};
    return {};
}

int get_topology(const char * topology) {
    if (!strcmp(topology, "points")) return GL_POINTS;
    if (!strcmp(topology, "lines")) return GL_LINES;
    if (!strcmp(topology, "line_loop")) return GL_LINE_LOOP;
    if (!strcmp(topology, "line_strip")) return GL_LINE_STRIP;
    if (!strcmp(topology, "triangles")) return GL_TRIANGLES;
    if (!strcmp(topology, "triangle_strip")) return GL_TRIANGLE_STRIP;
    if (!strcmp(topology, "triangle_fan")) return GL_TRIANGLE_FAN;
    return -1;
}

int count_mipmaps(int width, int height) {
    int size = width > height ? width : height;
    for (int i = 0; i < 32; ++i) {
        if (size <= (1 << i)) {
            return i;
        }
    }
    return 32;
}

PyObject * to_str(const unsigned char * ptr) {
    if (!ptr) {
        return PyUnicode_FromString("");
    }
    return PyUnicode_FromString((char *)ptr);
}

void * load_method(PyObject * context, const char * method) {
    PyObject * res = PyObject_CallMethod(context, "load", "s", method);
    if (!res) {
        if (!PyErr_Occurred()) {
            PyErr_Format(PyExc_Exception, "Cannot load %s", method);
        }
        return NULL;
    }
    return PyLong_AsVoidPtr(res);
}

GLMethods load_gl(PyObject * context) {
    GLMethods res = {};
    #define load(name) res.name = (gl ## name ## Proc)load_method(context, "gl" # name)
    load(ActiveTexture);
    load(AttachShader);
    load(BindBuffer);
    load(BindBufferRange);
    load(BindFramebuffer);
    load(BindRenderbuffer);
    load(BindSampler);
    load(BindTexture);
    load(BindVertexArray);
    load(BlendFuncSeparate);
    load(BlitFramebuffer);
    load(BufferData);
    load(BufferSubData);
    load(Clear);
    load(ClearColor);
    load(ClearDepth);
    load(ClearStencil);
    load(ColorMaski);
    load(CompileShader);
    load(CreateProgram);
    load(CreateShader);
    load(CullFace);
    load(DeleteBuffers);
    load(DeleteFramebuffers);
    load(DeleteProgram);
    load(DeleteRenderbuffersp);
    load(DeleteSamplers);
    load(DeleteShader);
    load(DeleteTextures);
    load(DeleteVertexArrays);
    load(DepthFunc);
    load(DepthMask);
    load(Disable);
    load(Disablei);
    load(DrawArraysInstanced);
    load(DrawBuffers);
    load(DrawElementsInstanced);
    load(Enable);
    load(Enablei);
    load(EnableVertexAttribArray);
    load(FramebufferRenderbuffer);
    load(FramebufferTexture2D);
    load(FrontFace);
    load(GenBuffers);
    load(GenerateMipmap);
    load(GenFramebuffers);
    load(GenRenderbuffers);
    load(GenSamplers);
    load(GenTextures);
    load(GenVertexArrays);
    load(GetActiveAttrib);
    load(GetActiveUniform);
    load(GetActiveUniformBlockiv);
    load(GetActiveUniformBlockName);
    load(GetAttribLocation);
    load(GetError);
    load(GetIntegerv);
    load(GetProgramInfoLog);
    load(GetProgramiv);
    load(GetShaderInfoLog);
    load(GetShaderiv);
    load(GetString);
    load(GetUniformBlockIndex);
    load(GetUniformLocation);
    load(LineWidth);
    load(LinkProgram);
    load(MapBufferRange);
    load(PointSize);
    load(PolygonOffset);
    load(PrimitiveRestartIndex);
    load(ReadBuffer);
    load(ReadPixels);
    load(RenderbufferStorageMultisample);
    load(SamplerParameterf);
    load(SamplerParameterfv);
    load(SamplerParameteri);
    load(ShaderSource);
    load(StencilFuncSeparate);
    load(StencilMaskSeparate);
    load(StencilOpSeparate);
    load(TexImage2D);
    load(TexImage3D);
    load(TexParameteri);
    load(TexSubImage2D);
    load(TexSubImage3D);
    load(Uniform1i);
    load(UniformBlockBinding);
    load(UnmapBuffer);
    load(UseProgram);
    load(VertexAttribDivisor);
    load(VertexAttribIPointer);
    load(VertexAttribPointer);
    load(Viewport);
    #undef load
    return res;
}

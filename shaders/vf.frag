#version 330 core
in vec3 vFragPosition;
//in vec2 vTexCoords;
in vec3 vNormal;

out vec4 color;

//uniform sampler2D tex;
//uniform bool cm_switch;


const float min_div = 0.0;
const float max_div = 3.0;



// some vector field (2d) : F = (sin x + x*sin(y) + x*sin(z)) * i + (sin y + y*sin(x) + y*sin(z)) * j +
//                          ( sin z + z*sin(x) + z*sin(y) ) * k

// 1st order derivatives to compute divergence (analytically)
float vfield_i_der( float x, float y, float z ) // dfx/dx
{
    return cos(x) + sin(y) + sin(z);
}

float vfield_j_der( float x, float y, float z ) //dfy/dy
{
    return sin(x) + cos(y) + sin(z);
}

float vfield_k_der( float x, float y, float z ) // dfz/dz
{
    return sin(x) + sin(y) + cos(z);
}

float divergence( float x, float y, float z )
{
    return vfield_i_der(x,y,z) + vfield_j_der(x,y,z) + vfield_k_der(x,y,z);
}



float der_z_y ( float x, float y, float z )
{
    return z * cos(y);
}

float der_y_z ( float x, float y, float z )
{
    return y * cos(z);
}

float der_x_z ( float x, float y, float z )
{
    return x * cos(z);
}

float der_z_x ( float x, float y, float z )
{
    return z * cos(x);
}

float der_y_x ( float x, float y, float z )
{
    return y * cos(x);
}

float der_x_y ( float x, float y, float z )
{
    return x * cos(y);
}


//sqrt( (z*cos y - y*cos(z)^2 + (x*cosz - z*cos(x))2 + (y*cos(x) + x*cos(y))2) );

float rot_magnitude( float x, float y, float z )
{
  vec3 rot = vec3( der_z_y(x,y,z) - der_y_z(x,y,z), der_x_z(x,y,z) - der_z_x(x,y,z), der_y_x(x,y,z) - der_x_y(x,y,z) );
  return length(rot);
}


float colormap_red(float x) {
    if (x < 100.0) {
        return (-9.55123422981038E-02 * x + 5.86981763554179E+00) * x - 3.13964093701986E+00;
    } else {
        return 5.25591836734694E+00 * x - 8.32322857142857E+02;
    }
}

float colormap_green(float x) {
    if (x < 150.0) {
        return 5.24448979591837E+00 * x - 3.20842448979592E+02;
    } else {
        return -5.25673469387755E+00 * x + 1.34195877551020E+03;
    }
}

float colormap_blue(float x) {
    if (x < 80.0) {
        return 4.59774436090226E+00 * x - 2.26315789473684E+00;
    } else {
        return -5.25112244897959E+00 * x + 8.30385102040816E+02;
    }
}

vec4 colormap(float x) {
    float t = x * 255.0;
    float r = clamp(colormap_red(t) / 255.0, 0.0, 1.0);
    float g = clamp(colormap_green(t) / 255.0, 0.0, 1.0);
    float b = clamp(colormap_blue(t) / 255.0, 0.0, 1.0);
    return vec4(r, g, b, 1.0);
}



void main()
{
  vec3 lightDir = vec3(1.0f, 1.0f, 0.0f);

//  vec3 sampled = texture(tex, vTexCoords).rgb;
//  float grayscale = 0.299f*sampled.r + 0.587f*sampled.g + 0.114*sampled.b;

  vec4 col;



  // y always == 0 ( 2d slice of 3d field )
  float div = divergence( vFragPosition.x, vFragPosition.z, vFragPosition.y );

  float normalized_div = (div - min_div) / (max_div - min_div);
// div should be normalized in [0;1]
  col = colormap( div );

  float kd = max(dot(vNormal, lightDir), 0.0);

  color = kd * col;
}
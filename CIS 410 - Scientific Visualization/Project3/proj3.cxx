#include <vtkImageData.h>
#include <vtkPNGWriter.h>
#include <vtkPointData.h>
#include <vtkPoints.h>
#include <vtkUnsignedCharArray.h>
#include <vtkFloatArray.h>
#include <vtkDataSetReader.h>
#include <vtkRectilinearGrid.h>
#include <vtkFloatArray.h>


// ****************************************************************************
//  Function: GetNumberOfPoints
//
//  Arguments:
//     dims: an array of size 3 with the number of points in X, Y, and Z.
//           2D data sets would have Z=1
//
//  Returns:  the number of points in a rectilinear mesh
//
// ****************************************************************************

int GetNumberOfPoints(const int *dims)
{
    // 3D
    //return dims[0]*dims[1]*dims[2];
    // 2D
    return dims[0]*dims[1];
}

// ****************************************************************************
//  Function: GetNumberOfCells
//
//  Arguments:
//
//      dims: an array of size 3 with the number of points in X, Y, and Z.
//            2D data sets would have Z=1
//
//  Returns:  the number of cells in a rectilinear mesh
//
// ****************************************************************************

int GetNumberOfCells(const int *dims)
{
    // 3D
    //return (dims[0]-1)*(dims[1]-1)*(dims[2]-1);
    // 2D
    return (dims[0]-1)*(dims[1]-1);
}


// ****************************************************************************
//  Function: GetPointIndex
//
//  Arguments:
//      idx:  the logical index of a point.
//              0 <= idx[0] < dims[0]
//              1 <= idx[1] < dims[1]
//              2 <= idx[2] < dims[2] (or always 0 if 2D)
//      dims: an array of size 3 with the number of points in X, Y, and Z.
//            2D data sets would have Z=1
//
//  Returns:  the point index
//
// ****************************************************************************

int GetPointIndex(const int *idx, const int *dims)
{
    // 3D
    //return idx[2]*dims[0]*dims[1]+idx[1]*dims[0]+idx[0];
    // 2D
    return idx[1]*dims[0]+idx[0];
}


// ****************************************************************************
//  Function: GetCellIndex
//
//  Arguments:
//      idx:  the logical index of a cell.
//              0 <= idx[0] < dims[0]-1
//              1 <= idx[1] < dims[1]-1 
//              2 <= idx[2] < dims[2]-1 (or always 0 if 2D)
//      dims: an array of size 3 with the number of points in X, Y, and Z.
//            2D data sets would have Z=1
//
//  Returns:  the cell index
//
// ****************************************************************************

int GetCellIndex(const int *idx, const int *dims)
{
    // 3D
    //return idx[2]*(dims[0]-1)*(dims[1]-1)+idx[1]*(dims[0]-1)+idx[0];
    // 2D
    return idx[1]*(dims[0]-1)+idx[0];
}

// ****************************************************************************
//  Function: GetLogicalPointIndex
//
//  Arguments:
//      idx (output):  the logical index of the point.
//              0 <= idx[0] < dims[0]
//              1 <= idx[1] < dims[1] 
//              2 <= idx[2] < dims[2] (or always 0 if 2D)
//      pointId:  a number between 0 and (GetNumberOfPoints(dims)-1).
//      dims: an array of size 3 with the number of points in X, Y, and Z.
//            2D data sets would have Z=1
//
//  Returns:  None (argument idx is output)
//
// ****************************************************************************

void GetLogicalPointIndex(int *idx, int pointId, const int *dims)
{
    // 3D
    // idx[0] = pointId%dim[0];
    // idx[1] = (pointId/dims[0])%dims[1];
    // idx[2] = pointId/(dims[0]*dims[1]);

    // 2D
    idx[0] = pointId%dims[0];
    idx[1] = pointId/dims[0];
}


// ****************************************************************************
//  Function: GetLogicalCellIndex
//
//  Arguments:
//      idx (output):  the logical index of the cell index.
//              0 <= idx[0] < dims[0]-1
//              1 <= idx[1] < dims[1]-1 
//              2 <= idx[2] < dims[2]-1 (or always 0 if 2D)
//      cellId:  a number between 0 and (GetNumberOfCells(dims)-1).
//      dims: an array of size 3 with the number of points in X, Y, and Z.
//            2D data sets would have Z=1
//
//  Returns:  None (argument idx is output)
//
// ****************************************************************************

void GetLogicalCellIndex(int *idx, int cellId, const int *dims)
{
    // 3D
    // idx[0] = cellId%(dims[0]-1);
    // idx[1] = (cellId/(dims[0]-1))%(dims[1]-1);
    // idx[2] = cellId/((dims[0]-1)*(dims[1]-1));

    // 2D
    idx[0] = cellId%(dims[0]-1);
    idx[1] = cellId/(dims[0]-1);
}

// ****************************************************************************
//  Function: EvaluateFieldAtLocation
//
//  Arguments:
//     pt: a two-dimensional location
//     dims: an array of size two.  
//              The first number is the size of the array in argument X, 
//              the second the size of Y.
//     X: an array (size is specified by dims).  
//              This contains the X locations of a rectilinear mesh.
//     Y: an array (size is specified by dims).  
//              This contains the Y locations of a rectilinear mesh.
//     F: a scalar field defined on the mesh.  Its size is dims[0]*dims[1].
//
//   Returns: the interpolated field value. 0 if the location is out of bounds.
//
// ****************************************************************************

float EvaluateFieldAtLocation(const float *pt, const int *dims, const float *X, 
                              const float *Y, const float *F)
{
    int x0 = 0;
    int x1 = 0;
    int y0 = 0;
    int y1 = 0;

    for(int i = 0; i < dims[0]; i++) {
        if(X[i] <= pt[0] && X[i+1] >= pt[0]) {
            x0 = i;
            x1 = i+1;
            break;
        }
    }
    for(int i = 0; i < dims[1]; i++) {
        if(Y[i] <= pt[1] && Y[i+1] >= pt[1]) {
            y0 = i;
            y1 = i+1;
            break;
        }
    }

    // t = (X-A)/(B-A)
    float tx = (pt[0] - X[x0]) / (X[x1] - X[x0]);

    // F(X) = F(A) + t*(F(B)-F(A))
    int pt1[2];
    int pt2[2];
    int pt3[2];
    int pt4[2];

    pt1[0] = x0;
    pt1[1] = y0;
    pt2[0] = x1;
    pt2[1] = y0;
    pt3[0] = x0;
    pt3[1] = y1;
    pt4[0] = x1;
    pt4[1] = y1;

    float fpt1 = F[GetPointIndex(pt1, dims)];
    float fpt2 = F[GetPointIndex(pt2, dims)];
    float fpt3 = F[GetPointIndex(pt3, dims)];
    float fpt4 = F[GetPointIndex(pt4, dims)];

    float fx1 = fpt1 + tx * (fpt2 - fpt1);
    float fx2 = fpt3 + tx * (fpt4 - fpt3);

    // t = (X-A)/(B-A)
    float ty = (pt[1] - Y[y0]) / (Y[y1] - Y[y0]);

    // F(X) = F(A) + t*(F(B)-F(A))
    float fx3 = fx1 + ty * (fx2 - fx1);

    if(!isnan(fx3)) {
        return fx3;
    }
    return 0;
}


void
WriteImage(vtkImageData *img, const char *filename)
{
    std::string full_filename = filename;
    full_filename += ".png";
    vtkPNGWriter *writer = vtkPNGWriter::New();
    writer->SetInputData(img);
    writer->SetFileName(full_filename.c_str());
    writer->Write();
    writer->Delete();
}

vtkImageData *
NewImage(int width, int height)
{
    vtkImageData *image = vtkImageData::New();
    image->SetDimensions(width, height, 1);
    //image->SetWholeExtent(0, width-1, 0, height-1, 0, 0);
    //image->SetUpdateExtent(0, width-1, 0, height-1, 0, 0);
    //image->SetNumberOfScalarComponents(3);
    image->AllocateScalars(VTK_UNSIGNED_CHAR, 3);
    //image->AllocateScalars();

    return image;
}

// ****************************************************************************
//  Function: ApplyBlueHotColorMap
//
//  Purpose: 
//     Maps a normalized scalar value F (0<=F<=1) to a color using the blue 
//     hot color map.
//
//     The blue hot color map has:
//        F=0: (0,0,128) 
//        F=1: (255,255,255) 
//       and smooth interpolation in between
//
//  Arguments:
//       F (input):     a scalar value between 0 and 1
//       RGB (output):  the location to store the color
//      
// ****************************************************************************

void
ApplyBlueHotColorMap(float F, unsigned char *RGB)
{
    RGB[0] = F * 255.0;
    RGB[1] = F * 255.0;
    RGB[2] = F * (255.0 - 128.0) + 128.0;
}


// ****************************************************************************
//  Function: ApplyDifferenceColorMap
//
//  Purpose: 
//     Maps a normalized scalar value F (0<=F<=1) to a color using a divergent colormap
//
//     The divergent color map has:
//        F=0: (0,0,128) 
//        F=0.5: (255,255,255) 
//        F=1: (128, 0, 0)
//       and smooth interpolation in between
//
//  Arguments:
//       F (input):     a scalar value between 0 and 1
//       RGB (output):  the location to store the color
//      
// ****************************************************************************
void
ApplyDifferenceColorMap(float F, unsigned char *RGB)
{
    if(F < 0.5) {
        float normalizedF = F / 0.5;
        float rg = normalizedF * 255.0;                 // Red & Green
        RGB[0] = rg;
        RGB[1] = rg;
        RGB[2] = normalizedF * (255.0 - 128.0) + 128.0; // Blue
    }
    else if(F == 0.5) {
        RGB[0] = 255;   // Red
        RGB[1] = 255;   // Green
        RGB[2] = 255;   // Blue
    }
    else {
        float normalizedF = (F - 0.5) / 0.5;
        float gb = normalizedF * -255.0 + 255.0;        // Green & Blue
        RGB[0] = normalizedF * (128.0 - 255.0) + 255.0; // Red
        RGB[1] = gb;
        RGB[2] = gb;
    }
}

// ****************************************************************************
//  Function: ApplyHSVColorMap
//
//  Purpose: 
//     Maps a normalized scalar value F (0<=F<=1) to a color using an HSV rainbow colormap
//
//     The rainbow colormap uses a saturation =1.0, value = 1.0, 
//     and interpolates hue from 0 to 360 degrees 
//
//  Arguments:
//       F (input):     a scalar value between 0 and 1
//       RGB (output):  the location to store the color
//      
// ****************************************************************************
void
ApplyHSVColorMap(float F, unsigned char *RGB)
{
    // Partially Taken from slide 39 of lecture 4
    float hue = F * 6.0;
    int i = floor(hue);
    float f = hue - i;
    float p = 0.0;  // 1.0 * (1.0 - 1.0);
    float q = 255.0 * (1.0 - 1.0 * f);
    float t = 255.0 * (1.0 - 1.0 * (1.0 - f));     

    float r = 0.0;
    float g = 0.0;
    float b = 0.0;

    switch(i) {
        case 0: 
            r = 255.0; 
            g = t; 
            b = p; 
            break;
        case 1: 
            r = q; 
            g = 255.0; 
            b = p; 
            break;
        case 2: 
            r = p; 
            g = 255.0; 
            b = t; 
            break;
        case 3: 
            r = p; 
            g = q; 
            b = 255.0; 
            break;
        case 4: 
            r = t; 
            g = p; 
            b = 255.0; 
            break;
        case 5: 
            r = 255.0; 
            g = p; 
            b = q; 
            break;
    }
    RGB[0] = r;
    RGB[1] = g;
    RGB[2] = b;
}


int main()
{
    int  i, j;

    vtkDataSetReader *rdr = vtkDataSetReader::New();
    rdr->SetFileName("proj3_data.vtk");
    rdr->Update();

    int dims[3];
    vtkRectilinearGrid *rgrid = (vtkRectilinearGrid *) rdr->GetOutput();
    rgrid->GetDimensions(dims);

    float *X = (float *) rgrid->GetXCoordinates()->GetVoidPointer(0);
    float *Y = (float *) rgrid->GetYCoordinates()->GetVoidPointer(0);
    float *F = (float *) rgrid->GetPointData()->GetScalars()->GetVoidPointer(0);
    
    int nx = 500;
    int ny = 500;

    vtkImageData *images[3];
    unsigned char *buffer[3];
    for (i = 0 ; i < 3 ; i++)
    {
        images[i] = NewImage(nx, ny);
        buffer[i] = (unsigned char *) images[i]->GetScalarPointer(0,0,0);
    }

    for (i = 0 ; i < 3*nx*ny ; i++)
        for (j = 0 ; j < 3 ; j++)
            buffer[j][i] = 0;

    for (i = 0 ; i < nx ; i++)
        for (j = 0 ; j < ny ; j++)
        {
            // ITERATE OVER PIXELS
            float pt[2];
            pt[0] = i / ((float)nx - 1.0) * 18.0 - 9.0;
            pt[1] = j / ((float)ny - 1.0) * 18.0 - 9.0;

            float f = EvaluateFieldAtLocation(pt, dims, X, Y, F);
            float normalizedF = (f - 1.2) / (5.02 - 1.2); //...; see step 5 re 1.2->5.02
            
            // I TAKE OVER HERE
            int offset = 3*(j*nx+i);
            ApplyBlueHotColorMap(normalizedF, buffer[0]+offset);
            ApplyDifferenceColorMap(normalizedF, buffer[1]+offset);
            ApplyHSVColorMap(normalizedF, buffer[2]+offset);
        }

    WriteImage(images[0], "bluehot");
    WriteImage(images[1], "difference");
    WriteImage(images[2], "hsv");
}


#include <vtkRenderWindow.h>
#include <vtkRenderer.h>
#include <vtkRenderWindowInteractor.h>
#include <vtkDataSetReader.h>
#include <vtkDataSetMapper.h>
#include <vtkContourFilter.h>
#include <vtkPlane.h>
#include <vtkCutter.h>
#include <vtkActor.h>
#include <vtkLookupTable.h>


int main(int argc, char *argv[])
{
   vtkDataSetReader *reader = vtkDataSetReader::New();
   reader->SetFileName("noise.vtk");
   reader->Update();

   // Referenced: https://vtk.org/Wiki/VTK/Examples/Cxx/VisualizationAlgorithms/Cutter

   // Plane
   vtkSmartPointer<vtkPlane> plane =
   vtkSmartPointer<vtkPlane>::New();
   plane->SetNormal(0,0,1);
   // Cutter
   vtkSmartPointer<vtkCutter> cutter = vtkSmartPointer<vtkCutter>::New();
   cutter->SetCutFunction(plane);
   cutter->SetInputConnection(reader->GetOutputPort());
   cutter->Update();

   vtkDataSetMapper *mapper = vtkDataSetMapper::New();
   mapper->SetInputConnection(cutter->GetOutputPort());
   
   vtkLookupTable *lut = vtkLookupTable::New();
   mapper->SetLookupTable(lut);
   mapper->SetScalarRange(1,6);
   lut->Build();

   vtkActor *actor = vtkActor::New();
   actor->SetMapper(mapper);

   vtkRenderer *ren = vtkRenderer::New();
   ren->AddActor(actor);

   vtkRenderWindow *renwin = vtkRenderWindow::New();
   renwin->AddRenderer(ren);

   vtkRenderWindowInteractor *iren = vtkRenderWindowInteractor::New();
   iren->SetRenderWindow(renwin);
   renwin->SetSize(768, 768); // 
   renwin->Render();
   iren->Start();

   reader->Delete();
   plane->Delete();
   // cutter->Delete();
   mapper->Delete();
   lut->Delete();
   actor->Delete();
   renwin->Delete();
   iren->Delete();
}



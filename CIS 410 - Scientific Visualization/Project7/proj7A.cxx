
#include <vtkRenderWindow.h>
#include <vtkRenderer.h>
#include <vtkRenderWindowInteractor.h>
#include <vtkDataSetReader.h>
#include <vtkDataSetMapper.h>
#include <vtkActor.h>
#include <vtkLookupTable.h>


int main(int argc, char *argv[])
{
   vtkDataSetReader *reader = vtkDataSetReader::New();
   reader->SetFileName("noise.vtk");
   reader->Update();

   vtkDataSetMapper *mapper = vtkDataSetMapper::New();
   mapper->SetInputData(reader->GetOutput());
   
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
   mapper->Delete();
   lut->Delete();
   actor->Delete();
   renwin->Delete();
   iren->Delete();
}



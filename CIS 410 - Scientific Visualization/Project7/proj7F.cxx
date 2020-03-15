
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

	// Contour Filter
	vtkContourFilter *cf = vtkContourFilter::New();
	cf->SetNumberOfContours(2);
	cf->SetValue(0, 2.4);
	cf->SetValue(1, 4.0);
	cf->SetInputConnection(reader->GetOutputPort());

	vtkDataSetMapper *mapper1 = vtkDataSetMapper::New();
	mapper1->SetInputConnection(cutter->GetOutputPort());
	vtkDataSetMapper *mapper2 = vtkDataSetMapper::New();
	mapper2->SetInputConnection(cf->GetOutputPort());

	vtkLookupTable *lut = vtkLookupTable::New();
	mapper1->SetLookupTable(lut);
	mapper1->SetScalarRange(1,6);
	mapper2->SetLookupTable(lut);
	mapper2->SetScalarRange(1,6);
	lut->Build();

	// Interpolate from blue to red
	for(int i = 0; i < 256; i++) {
		lut->SetTableValue(i, i, 0.0, 256.0 - i, 1.0);
	}
	
	vtkActor *actor1 = vtkActor::New();
	actor1->SetMapper(mapper1);
	vtkActor *actor2 = vtkActor::New();
	actor2->SetMapper(mapper2);

	vtkRenderer *ren1 = vtkRenderer::New();
	vtkRenderer *ren2 = vtkRenderer::New();
	ren1->AddActor(actor1);
	ren2->AddActor(actor2);

	double xmins[2] = {0.0, 0.5};
	double xmaxs[2] = {0.5, 1.0};
	double ymins[2] = {0.0, 0.0};
	double ymaxs[2] = {1.0, 1.0};

	vtkRenderWindow *renwin = vtkRenderWindow::New();
	renwin->AddRenderer(ren1);
	renwin->AddRenderer(ren2);

	ren1->SetViewport(xmins[0],ymins[0],xmaxs[0],ymaxs[0]);
	ren2->SetViewport(xmins[1],ymins[1],xmaxs[1],ymaxs[1]);

	vtkRenderWindowInteractor *iren = vtkRenderWindowInteractor::New();
	iren->SetRenderWindow(renwin);
	renwin->SetSize(768, 768); // 
	renwin->Render();
	iren->Start();

	reader->Delete();
	plane->Delete();
	cf->Delete();
	mapper1->Delete();
	mapper2->Delete();
	lut->Delete();
	actor1->Delete();
	actor2->Delete();
	renwin->Delete();
	iren->Delete();
}



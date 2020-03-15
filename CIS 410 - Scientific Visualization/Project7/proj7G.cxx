
#include <vtkRenderWindow.h>
#include <vtkRenderer.h>
#include <vtkRenderWindowInteractor.h>
#include <vtkDataSetReader.h>
#include <vtkDataSetMapper.h>
#include <vtkContourFilter.h>
#include <vtkPlane.h>
#include <vtkCutter.h>
#include <vtkActor.h>
#include <vtkCamera.h>
#include <vtkCallbackCommand.h>
#include <vtkLookupTable.h>

vtkRenderWindow *renwin = NULL;
vtkContourFilter *cf = NULL;
vtkRenderer *ren2 = NULL;
vtkRenderer *ren1 = NULL;

void Animate(vtkObject*caller, unsigned long eid, void* clientdata, void *calldata) {
	// Taken From Piazza

	// 'a' key must be pressed to begin animation
    vtkRenderWindowInteractor *iren = static_cast<vtkRenderWindowInteractor*>(caller);
	if (iren->GetKeySym()[0] != 'a') {
		return;
	}

	// Animate
	double isovalue = 1.0;
	for(int i = 0; i < 500; i++) {
		cf->Update();
		cf->SetValue(0, isovalue);
		cf->Update();

		isovalue += 0.01;
		
		ren2->GetActiveCamera()->ShallowCopy(ren1->GetActiveCamera());
		renwin->Render();
    }
}

int main(int argc, char *argv[])
{
	vtkDataSetReader *reader = vtkDataSetReader::New();
	reader->SetFileName("noise.vtk");
	reader->Update();

	// Referenced: https://vtk.org/Wiki/VTK/Examples/Cxx/VisualizationAlgorithms/Cutter
	// Plane
	vtkSmartPointer<vtkPlane> plane = vtkSmartPointer<vtkPlane>::New();
	plane->SetNormal(0,0,1);
	// Cutter
	vtkSmartPointer<vtkCutter> cutter = vtkSmartPointer<vtkCutter>::New();
	cutter->SetCutFunction(plane);
	cutter->SetInputConnection(reader->GetOutputPort());
	cutter->Update();

	double isovalue = 1.0;
	// Contour Filter
	cf = vtkContourFilter::New();
	cf->SetNumberOfContours(1);
	cf->SetValue(0, isovalue);
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

	ren1 = vtkRenderer::New();
	ren2 = vtkRenderer::New();
	ren1->AddActor(actor1);
	ren2->AddActor(actor2);

	double xmins[2] = {0.0, 0.5};
	double xmaxs[2] = {0.5, 1.0};
	double ymins[2] = {0.0, 0.0};
	double ymaxs[2] = {1.0, 1.0};

	renwin = vtkRenderWindow::New();
	renwin->AddRenderer(ren1);
	renwin->AddRenderer(ren2);

	ren1->SetViewport(xmins[0],ymins[0],xmaxs[0],ymaxs[0]);
	ren2->SetViewport(xmins[1],ymins[1],xmaxs[1],ymaxs[1]);

	vtkRenderWindowInteractor *iren = vtkRenderWindowInteractor::New();
	iren->SetRenderWindow(renwin);
	renwin->SetSize(768, 768); // 
	renwin->Render();

	// 'a' key must be pressed to begin animation
	vtkSmartPointer<vtkCallbackCommand> keypressCallback = vtkSmartPointer<vtkCallbackCommand>::New();
	keypressCallback->SetCallback(Animate);
	iren->AddObserver(vtkCommand::KeyPressEvent, keypressCallback);

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



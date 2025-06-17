from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from experiments.models import Device, Experiment

User = get_user_model()

class MethodsTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='user', password='password1234')
        self.client.login(username='user', password='password1234')

        self.device1 = Device.objects.create(brand='brand', model='model')
        self.device2 = Device.objects.create(brand='brand', model='model1')
        self.device3 = Device.objects.create(brand='brand1', model='model2')

        self.exp1 = Experiment.objects.create(device=self.device1, mode='photo')
        self.exp2 = Experiment.objects.create(device=self.device1, mode='video')
        self.exp3 = Experiment.objects.create(device=self.device2, mode='photo')

    def test_get_models(self):
        response = self.client.get(reverse('experiments:get-models'), {'brand': 'brand'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('models', data)
        self.assertCountEqual(data['models'], ['model', 'model1'])  # modelli corretti

        response = self.client.get(reverse('experiments:get-models'), {'brand': 'NonExistentBrand'})
        data = response.json()
        self.assertEqual(data['models'], [])

    def test_get_experiments_by_device(self):
        response = self.client.get(reverse('experiments:get_experiments'), {'brand': 'brand', 'model': 'model'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('experiments', data)
        self.assertEqual(len(data['experiments']), 2)

        for exp in data['experiments']:
            self.assertIn('id', exp)
            self.assertIn('label', exp)

        response = self.client.get(reverse('experiments:get_experiments'), {'brand': 'brand1', 'model': 'model1'})
        data = response.json()
        self.assertEqual(len(data['experiments']), 0)

    def test_get_experiment_notes(self):
        response = self.client.get(reverse('experiments:get_experiment_notes'), {'experiment_id': self.exp1.id})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('notes', data)
        self.assertEqual(data['notes'], '') 

        response = self.client.get(reverse('experiments:get_experiment_notes'), {'experiment_id': 99999})
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertEqual(data['notes'], '')

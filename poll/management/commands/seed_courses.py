from django.core.management.base import BaseCommand
from poll.models import Course


class Command(BaseCommand):
    help = 'Seed initial Value-Added Courses for ECE Department'

    def handle(self, *args, **options):
        courses_data = [
            {
                'name': 'OOPS and C++',
                'description': 'Object-Oriented Programming concepts using C++',
                'icon': '💻',
                'color': '#6366f1',
                'syllabus': '''
<h4>Module 1: Introduction to OOP</h4>
<ul>
    <li>Basic concepts of Object-Oriented Programming</li>
    <li>Classes and Objects</li>
    <li>Data abstraction and encapsulation</li>
    <li>Inheritance and Polymorphism</li>
</ul>

<h4>Module 2: C++ Fundamentals</h4>
<ul>
    <li>C++ syntax and structure</li>
    <li>Variables, data types, and operators</li>
    <li>Control structures and functions</li>
    <li>Arrays, pointers, and references</li>
</ul>

<h4>Module 3: Classes and Objects in C++</h4>
<ul>
    <li>Class definition and object creation</li>
    <li>Constructors and destructors</li>
    <li>Friend functions and classes</li>
    <li>Static members</li>
</ul>

<h4>Module 4: Inheritance and Polymorphism</h4>
<ul>
    <li>Types of inheritance</li>
    <li>Virtual functions and abstract classes</li>
    <li>Function overloading and overriding</li>
    <li>Operator overloading</li>
</ul>

<h4>Module 5: Advanced Topics</h4>
<ul>
    <li>Templates and generic programming</li>
    <li>Exception handling</li>
    <li>File handling in C++</li>
    <li>Standard Template Library (STL)</li>
</ul>
'''
            },
            {
                'name': 'System Verilog',
                'description': 'Hardware Description Language for VLSI Design',
                'icon': '🔌',
                'color': '#8b5cf6',
                'syllabus': '''
<h4>Module 1: Introduction to SystemVerilog</h4>
<ul>
    <li>Evolution from Verilog to SystemVerilog</li>
    <li>Data types and operators</li>
    <li>SystemVerilog enhancements</li>
    <li>Design and verification constructs</li>
</ul>

<h4>Module 2: Data Types and Operators</h4>
<ul>
    <li>Two-state and four-state data types</li>
    <li>Arrays: fixed, dynamic, associative, and queues</li>
    <li>Structures and unions</li>
    <li>Type casting and conversion</li>
</ul>

<h4>Module 3: Procedural Blocks and Control Flow</h4>
<ul>
    <li>Always blocks: always_comb, always_ff, always_latch</li>
    <li>Unique and priority case statements</li>
    <li>Loops and control statements</li>
    <li>Tasks and functions</li>
</ul>

<h4>Module 4: Object-Oriented Programming in SystemVerilog</h4>
<ul>
    <li>Classes and objects</li>
    <li>Inheritance and polymorphism</li>
    <li>Virtual methods and abstract classes</li>
    <li>Randomization constraints</li>
</ul>

<h4>Module 5: Verification Methodology</h4>
<ul>
    <li>Assertions and functional coverage</li>
    <li>Testbench architecture</li>
    <li>Interface and modport</li>
    <li>Introduction to UVM basics</li>
</ul>
'''
            },
            {
                'name': 'Machine Learning for Signal & Image Processing using Raspberry Pi',
                'description': 'Practical ML applications on embedded systems',
                'icon': '🤖',
                'color': '#10b981',
                'syllabus': '''
<h4>Module 1: Introduction to Machine Learning</h4>
<ul>
    <li>Basics of Machine Learning</li>
    <li>Types: Supervised, Unsupervised, Reinforcement Learning</li>
    <li>Python for ML: NumPy, Pandas, Scikit-learn</li>
    <li>Introduction to Raspberry Pi setup</li>
</ul>

<h4>Module 2: Signal Processing Fundamentals</h4>
<ul>
    <li>Digital signal processing basics</li>
    <li>Time and frequency domain analysis</li>
    <li>Filters: FIR and IIR</li>
    <li>Audio signal processing on Raspberry Pi</li>
</ul>

<h4>Module 3: Image Processing Basics</h4>
<ul>
    <li>Digital image fundamentals</li>
    <li>Image enhancement and filtering</li>
    <li>Edge detection and segmentation</li>
    <li>OpenCV on Raspberry Pi</li>
</ul>

<h4>Module 4: ML for Signal Processing</h4>
<ul>
    <li>Feature extraction from signals</li>
    <li>Classification of audio signals</li>
    <li>Speech recognition basics</li>
    <li>Real-time signal classification on Pi</li>
</ul>

<h4>Module 5: ML for Image Processing</h4>
<ul>
    <li>Convolutional Neural Networks (CNN)</li>
    <li>Object detection and recognition</li>
    <li>Face detection and recognition</li>
    <li>Deploying ML models on Raspberry Pi</li>
</ul>
'''
            },
            {
                'name': 'Embedded Systems and IoT',
                'description': 'Design and development of IoT-enabled embedded systems',
                'icon': '📡',
                'color': '#f59e0b',
                'syllabus': '''
<h4>Module 1: Embedded Systems Fundamentals</h4>
<ul>
    <li>Introduction to embedded systems</li>
    <li>Microcontrollers vs Microprocessors</li>
    <li>ARM architecture basics</li>
    <li>Development environments and tools</li>
</ul>

<h4>Module 2: Microcontroller Programming</h4>
<ul>
    <li>GPIO programming</li>
    <li>Timers and interrupts</li>
    <li>Serial communication: UART, SPI, I2C</li>
    <li>ADC and DAC interfaces</li>
</ul>

<h4>Module 3: Introduction to IoT</h4>
<ul>
    <li>IoT architecture and protocols</li>
    <li>MQTT and CoAP protocols</li>
    <li>Cloud platforms: AWS IoT, ThingSpeak</li>
    <li>Node-RED for IoT applications</li>
</ul>

<h4>Module 4: Sensors and Actuators</h4>
<ul>
    <li>Types of sensors: Temperature, Humidity, Motion</li>
    <li>Sensor interfacing and calibration</li>
    <li>Actuator control: Motors, Relays</li>
    <li>Building sensor networks</li>
</ul>

<h4>Module 5: IoT Projects</h4>
<ul>
    <li>Smart home automation</li>
    <li>Environmental monitoring system</li>
    <li>Wearable health devices</li>
    <li>Industrial IoT applications</li>
</ul>
'''
            },
            {
                'name': '5G Communication',
                'description': 'Next-generation wireless communication technologies',
                'icon': '📶',
                'color': '#ef4444',
                'syllabus': '''
<h4>Module 1: Evolution of Mobile Communication</h4>
<ul>
    <li>1G to 5G: Evolution overview</li>
    <li>5G use cases and requirements</li>
    <li>5G NR (New Radio) specifications</li>
    <li>IMT-2020 standards</li>
</ul>

<h4>Module 2: 5G Network Architecture</h4>
<ul>
    <li>5G Core Network (5GC) architecture</li>
    <li>Service-based architecture</li>
    <li>Network slicing concepts</li>
    <li>Edge computing and MEC</li>
</ul>

<h4>Module 3: 5G Physical Layer</h4>
<ul>
    <li>OFDM and waveform design</li>
    <li>Massive MIMO technology</li>
    <li>Beamforming techniques</li>
    <li>Millimeter wave communication</li>
</ul>

<h4>Module 4: 5G Protocols and Procedures</h4>
<ul>
    <li>Radio resource management</li>
    <li>Initial access and mobility</li>
    <li>Quality of Service (QoS) framework</li>
    <li>Security in 5G networks</li>
</ul>

<h4>Module 5: 5G Applications and Future</h4>
<ul>
    <li>Enhanced Mobile Broadband (eMBB)</li>
    <li>Ultra-Reliable Low-Latency Communication (URLLC)</li>
    <li>Massive Machine-Type Communication (mMTC)</li>
    <li>6G vision and research directions</li>
</ul>
'''
            }
        ]

        for course_data in courses_data:
            course, created = Course.objects.get_or_create(
                name=course_data['name'],
                defaults={
                    'description': course_data['description'],
                    'icon': course_data['icon'],
                    'color': course_data['color'],
                    'syllabus': course_data['syllabus'],
                    'max_capacity': 50,
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created course: {course.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'⚠ Course already exists: {course.name}')
                )

        self.stdout.write(self.style.SUCCESS('\n✅ Successfully seeded all courses!'))

import 'dart:async';
import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:app_links/app_links.dart';
import 'core/router/app_router.dart';
import 'core/theme/app_theme.dart';
import 'core/utils/app_bloc_observer.dart';
import 'injection/injection_container.dart' as di;

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  Bloc.observer = const AppBlocObserver();

  // Initialize Firebase — pastikan google-services.json/GoogleService-Info.plist sudah ada
  await Firebase.initializeApp();

  // Initialize dependency injection
  await di.init();

  // Set preferred orientations
  await SystemChrome.setPreferredOrientations([
    DeviceOrientation.portraitUp,
    DeviceOrientation.portraitDown,
  ]);

  // Status bar style
  SystemChrome.setSystemUIOverlayStyle(const SystemUiOverlayStyle(
    statusBarColor: Colors.transparent,
    statusBarIconBrightness: Brightness.dark,
  ));

  runApp(const DompetKampusApp());
}

class DompetKampusApp extends StatefulWidget {
  const DompetKampusApp({super.key});

  @override
  State<DompetKampusApp> createState() => _DompetKampusAppState();
}

class _DompetKampusAppState extends State<DompetKampusApp> {
  final _appLinks = AppLinks();
  StreamSubscription<Uri>? _linkSubscription;

  @override
  void initState() {
    super.initState();
    _initDeepLinks();
  }

  void _initDeepLinks() {
    _linkSubscription = _appLinks.uriLinkStream.listen((uri) {
      // Tangkap semua URL dkg://... dan teruskan path + query ke GoRouter
      if (uri.scheme == 'dkg') {
        final path = uri.path.isNotEmpty ? uri.path : '/${uri.host}';
        final query = uri.query.isNotEmpty ? '?${uri.query}' : '';
        AppRouter.router.go('$path$query');
      }
    });
  }

  @override
  void dispose() {
    _linkSubscription?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      title: 'Dompet Kampus Global',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.light,
      routerConfig: AppRouter.router,
    );
  }
}
